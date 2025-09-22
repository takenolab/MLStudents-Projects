import pandas as pd
import matplotlib.pyplot as plt
import uuid
import os
from pathlib import Path
import numpy as np
import pydantic
from typing import List, Dict, Optional, Union, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CSVGraphGenerator:
    def __init__(self):
        self.df = None
        self.numeric_columns = []
        self.categorical_columns = []
        self.datetime_columns = []
        self.original_columns_count = 0
        
    def validate_csv_file(self, file_path: str) -> bool:
        try:
            if not Path(file_path).exists():
                raise FileNotFoundError(f"File {file_path} does not exist")
            
            if not file_path.lower().endswith('.csv'):
                raise ValueError("File must be a CSV file")
            
            file_size = Path(file_path).stat().st_size
            if file_size > 50 * 1024 * 1024:  # 50MB limit
                raise ValueError("File size exceeds 50MB limit")
                
            return True
            
        except Exception as e:
            logger.error(f"File validation failed: {e}")
            raise
    
    def detect_data_types(self) -> Dict[str, str]:
        """Detect and categorize data types for each column"""
        type_mapping = {}
        
        for column in self.df.columns:
         
            non_null_count = self.df[column].count()
            total_count = len(self.df[column])
            
            if non_null_count == 0:
                type_mapping[column] = 'empty'
                continue
            
          
            try:
                numeric_test = pd.to_numeric(self.df[column].dropna(), errors='coerce')
                if not numeric_test.isna().all():
                    type_mapping[column] = 'numeric'
                    continue
            except:
                pass
            
            
            try:
                datetime_test = pd.to_datetime(self.df[column].dropna(), errors='coerce')
                if not datetime_test.isna().all():
                    type_mapping[column] = 'datetime'
                    continue
            except:
                pass
            
            
            if self.df[column].dropna().isin([True, False, 'True', 'False', 1, 0]).all():
                type_mapping[column] = 'boolean'
                continue
            
             
            type_mapping[column] = 'categorical'
        
        return type_mapping
    
    def handle_empty_columns(self, threshold: float = 0.9) -> Tuple[List[str], List[str]]:
        """
        Handle empty columns based on missing data threshold
        Returns: (deleted_columns, kept_columns)
        """
        empty_columns = []
        kept_columns = []
        
        for column in self.df.columns:
            non_null_count = self.df[column].count()
            null_percentage = 1 - (non_null_count / len(self.df))
            
            if null_percentage >= threshold:
                empty_columns.append(column)
            else:
                kept_columns.append(column)
        
        # Delete empty columns if they are less than 10
        if len(empty_columns) > 0 and len(empty_columns) <= 10:
            logger.info(f"Deleting {len(empty_columns)} empty columns: {empty_columns}")
            self.df = self.df.drop(columns=empty_columns)
            return (empty_columns, kept_columns)
        elif len(empty_columns) > 10:
            logger.warning(f"Too many empty columns ({len(empty_columns)}). Keeping all columns.")
            return ([], self.df.columns.tolist())
        else:
            return ([], self.df.columns.tolist())
    
    def analyze_column_statistics(self) -> Dict:
        """Analyze and return detailed statistics for each column"""
        stats = {}
        
        for column in self.df.columns:
            col_stats = {
                'dtype': str(self.df[column].dtype),
                'non_null_count': self.df[column].count(),
                'null_count': self.df[column].isnull().sum(),
                'null_percentage': (self.df[column].isnull().sum() / len(self.df)) * 100,
                'unique_values': self.df[column].nunique(),
            }
            
            if column in self.numeric_columns:
                col_stats.update({
                    'min': self.df[column].min(),
                    'max': self.df[column].max(),
                    'mean': self.df[column].mean(),
                    'std': self.df[column].std()
                })
            
            stats[column] = col_stats
        
        return stats
    
    def load_and_validate_data(self, file_path: str, empty_column_threshold: float = 0.9) -> bool:
        try:
            # Load CSV file with better handling
            self.df = pd.read_csv(file_path, low_memory=False)
            self.original_columns_count = len(self.df.columns)
            
            # Check number of columns
            if len(self.df.columns) > 200:
                raise ValueError("Number of columns exceeds 200 limit")
            
            if len(self.df.columns) < 6:
                raise ValueError("Number of columns must be at least 6")
            
            # Check for empty dataframe
            if self.df.empty:
                raise ValueError("CSV file is empty")
            
            # Check for sufficient rows
            if len(self.df) < 2:
                raise ValueError("CSV file must contain at least 2 rows")
            
            # Detect data types
            data_types = self.detect_data_types()
            logger.info(f"Detected data types: {data_types}")
            
            # Handle empty columns
            deleted_cols, kept_cols = self.handle_empty_columns(empty_column_threshold)
            
            if deleted_cols:
                logger.info(f"Deleted {len(deleted_cols)} empty columns")
            elif len([col for col, dtype in data_types.items() if dtype == 'empty']) > 10:
                logger.warning("More than 10 empty columns detected but not deleted due to threshold")
            
            # Update column categorization after handling empty columns
            self.numeric_columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
            self.categorical_columns = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
            self.datetime_columns = self.df.select_dtypes(include=['datetime64']).columns.tolist()
            
            # Convert potential datetime columns
            for col in self.df.columns:
                if col not in self.numeric_columns and col not in self.categorical_columns:
                    try:
                        self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                        if not self.df[col].isna().all():
                            self.datetime_columns.append(col)
                    except:
                        pass
            
            # Check if we have sufficient data for graphing
            if not self.numeric_columns:
                raise ValueError("No numeric columns found in the dataset after processing")
            
            if not self.categorical_columns and not self.datetime_columns:
                logger.warning("No categorical or datetime columns found for X-axis")
            
            # Analyze column statistics
            column_stats = self.analyze_column_statistics()
            logger.info("Column statistics analysis completed")
            
            logger.info(f"Loaded data with {len(self.df)} rows and {len(self.df.columns)} columns")
            logger.info(f"Original columns: {self.original_columns_count}, Current columns: {len(self.df.columns)}")
            logger.info(f"Numeric columns: {self.numeric_columns}")
            logger.info(f"Categorical columns: {self.categorical_columns}")
            logger.info(f"Datetime columns: {self.datetime_columns}")
            
            return True
            
        except Exception as e:
            logger.error(f"Data validation failed: {e}")
            raise
    
    def get_data_summary(self) -> Dict:
        """Return a comprehensive summary of the data"""
        if self.df is None:
            return {}
        
        summary = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'original_columns': self.original_columns_count,
            'numeric_columns': self.numeric_columns,
            'categorical_columns': self.categorical_columns,
            'datetime_columns': self.datetime_columns,
            'missing_values_per_column': self.df.isnull().sum().to_dict(),
            'data_types': {col: str(self.df[col].dtype) for col in self.df.columns}
        }
        
        return summary
    
    def create_bar_chart(self, x_column: str, y_column: str, title: str = "Bar Chart",  label: Optional[str] = None):
        """
        Create a bar chart with modern dark theme.
        """
        try:
            figsize: tuple = (10, 6)
            color: str = 'skyblue'
            if x_column not in self.df.columns or y_column not in self.df.columns:
                raise ValueError("Specified columns not found in dataframe")

            if y_column not in self.numeric_columns:
                raise ValueError("Y-axis column must be numeric")

            # Prepare data
            data = self.df[[x_column, y_column]].dropna()

            # Dark theme
            plt.style.use("dark_background")
            fig, ax = plt.subplots(figsize=figsize)
            fig.patch.set_facecolor('#121212')
            ax.set_facecolor('#121212')

            # Bar chart
            bar_label = label or y_column
            ax.bar(data[x_column], data[y_column], color=color, label=bar_label)

            # Grid
            ax.grid(True, linestyle='--', alpha=0.3, color='gray')

            # Labels and title
            ax.set_title(title, color='white')
            ax.set_xlabel(x_column, color='white')
            ax.set_ylabel(y_column, color='white')

            # Rotate x-axis labels for readability
            ax.tick_params(axis='x', rotation=45, colors='white')
            ax.tick_params(axis='y', colors='white')

            # Legend (optional)
            ax.legend(loc='upper right', facecolor='#1e1e1e', edgecolor='white', labelcolor='white')

            plt.tight_layout()
            filename = f"bar_chart_{uuid.uuid4().hex}.png"
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close(fig)

            return str(filename)

        except Exception as e:
            logger.error(f"Error creating bar chart: {e}")
            raise

    
    def create_scatter_plot(self, x_column: str, y_column: str, title: str = "Scatter Plot",label: Optional[str] = None):
        """
        Create a scatter plot with modern dark styling.
        """
        try:
            figsize: tuple = (10, 6)
            color= 'blue'
            alpha= 0.6, 
            if x_column not in self.numeric_columns or y_column not in self.numeric_columns:
                raise ValueError("Both X and Y columns must be numeric for scatter plot")

            # Sort for visual consistency (optional, not required for scatter)
            data = self.df[[x_column, y_column]].dropna()

            # Apply dark style
            plt.style.use("dark_background")
            fig, ax = plt.subplots(figsize=figsize)
            fig.patch.set_facecolor('#121212')
            ax.set_facecolor('#121212')

            # Scatter plot
            scatter_label = label or f"{y_column} vs {x_column}"
            ax.scatter(data[x_column], data[y_column], color=color, alpha=alpha, label=scatter_label)

            # Grid
            ax.grid(True, linestyle='--', color='gray', alpha=0.3)

            # Labels & title
            ax.set_title(title, color='white')
            ax.set_xlabel(x_column, color='white')
            ax.set_ylabel(y_column, color='white')

            # Tick color
            ax.tick_params(colors='white')

            # Optional legend
            ax.legend(loc='upper right', facecolor='#1e1e1e', edgecolor='white', labelcolor='white')

            plt.tight_layout()
            filename = f"bar_scatter_{uuid.uuid4().hex}.png"
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close(fig)

            return str(filename)

        except Exception as e:
            logger.error(f"Error creating scatter plot: {e}")
            raise

    
    def create_line_chart(self, x_column: str, y_column: str, title: str = "Line Chart",label: Optional[str] = None):
        """
        Create a modern styled line chart with dark theme.
        """
        try:
            figsize: tuple = (10, 6) 
            color: str = 'red'
            linewidth: float = 2, 
            if x_column not in self.df.columns or y_column not in self.df.columns:
                raise ValueError("Specified columns not found in dataframe")

            if y_column not in self.numeric_columns:
                raise ValueError("Y-axis column must be numeric")

         
            sorted_df = self.df.sort_values(by=x_column)

         
            plt.style.use("dark_background")
            fig, ax = plt.subplots(figsize=figsize)
            fig.patch.set_facecolor('#121212')
            ax.set_facecolor('#121212')

     
            plot_label = label or y_column
            ax.plot(sorted_df[x_column], sorted_df[y_column], color=color, linewidth=linewidth, label=plot_label)

        
            ax.grid(True, linestyle='--', alpha=0.3, color='gray')

          
            ax.set_title(title, color='white')
            ax.set_xlabel(x_column, color='white')
            ax.set_ylabel(y_column, color='white')

  
            ax.tick_params(colors='white')

    
            ax.legend(loc='upper left', facecolor='#1e1e1e', edgecolor='white', labelcolor='white')

           
            plt.tight_layout()
                    

            filename = f"bar_line_{uuid.uuid4().hex}.png"
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close(fig)

            return str(filename)

        except Exception as e:
            logger.error(f"Error creating bar chart: {e}")
            raise

  

    def create_pie_chart(self, column: str, title: str = "Pie Chart"):
     
        try:
            figsize: tuple = (8, 8)
            autopct: str = '%1.1f%%'
            if column not in self.df.columns:
                raise ValueError("Specified column not found in dataframe")
    
            value_counts = self.df[column].value_counts()

            
            if len(value_counts) > 10:
                value_counts = value_counts.head(10)
                logger.warning(f"Too many categories. Showing top 10 for '{column}'.")

        
            plt.style.use("dark_background")
            fig, ax = plt.subplots(figsize=figsize)
            fig.patch.set_facecolor('#121212') 
            ax.set_facecolor('#121212')

            
            colors = plt.cm.tab10.colors if len(value_counts) <= 10 else plt.cm.Set3.colors

        
            wedges, texts, autotexts = ax.pie(
                value_counts.values,
                labels=None, 
                autopct=autopct,
                startangle=90,
                colors=colors,
                textprops={'color': 'white'}
            )

            
            ax.axis('equal')

        
            ax.legend(
                wedges,
                value_counts.index,
                title=column,
                loc='center left',
                bbox_to_anchor=(1, 0.5),
                facecolor='#1e1e1e',
                edgecolor='white',
                labelcolor='white'
            )

    
            ax.set_title(title, color='white')

        
            plt.tight_layout()
            filename = f"bar_pie_{uuid.uuid4().hex}.png"
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close(fig)

            return str(filename)

        except Exception as e:
            logger.error(f"Error creating pie chart: {e}")
            raise

    
    def create_graph_from_csv(self, file_path: str, graph_type: str, empty_column_threshold: float = 0.9, **kwargs):
        try:
          
            self.validate_csv_file(file_path)
            
     
            self.load_and_validate_data(file_path, empty_column_threshold)
            
         
            if graph_type == 'bar':
               return str(self.create_bar_chart(**kwargs))
            elif graph_type == 'scatter':
               return str(self.create_scatter_plot(**kwargs))
            elif graph_type == 'line':
              return  str(self.create_line_chart(**kwargs))
            elif graph_type == 'pie':
               return str(self.create_pie_chart(**kwargs))
            else:
                return "Invalid graph type. Choose from: 'bar', 'scatter', 'line', 'pie'"
                
        except Exception as e:
            logger.error(f"Error creating graph: {e}")
            raise
 
 
 
graph_generator = CSVGraphGenerator()
 
file_path = 'data/sales_data.csv'


def generate_graph(file_path: str, graph_type: str, x_column: str, y_column: str, title: str, label: str, column: str) -> str:
    """
    Generate a graph based on the provided CSV file and the specified graph type.

    This function supports the following graph types:
    - 'bar': Creates a bar chart.
    - 'scatter': Creates a scatter plot.
    - 'line': Creates a line chart.
    - 'pie': Creates a pie chart.

    The function uses the `graph_generator.create_graph_from_csv()` method to create the graph and save it as a PNG file. It returns the file path of the generated graph. In case of an error, it returns a descriptive error message.

    Args:
        file_path (str): Path to the CSV file to be used for generating the graph.
        graph_type (str): Type of the graph to be generated. Options are 'bar', 'scatter', 'line', 'pie'.
        x_column (str): The name of the column to be used for the X-axis (for 'bar', 'scatter', and 'line' types).
        y_column (str): The name of the column to be used for the Y-axis (for 'bar', 'scatter', and 'line' types).
        title (str): Title of the graph.
        label (str): Label for the Y-axis or the series in the chart.
        column (str): The name of the column to be used for the pie chart's slices (only for 'pie' type) only.

    Returns:
        str: The file path of the generated graph image (PNG format). If there is an error, returns an error message.
        
    Raises:
        ValueError: If the `graph_type` is invalid or if there are issues with the CSV file or columns.
    """


    if graph_type == 'bar':  
        try:
            bar_chart_file = graph_generator.create_graph_from_csv(
                file_path=file_path,
                graph_type=graph_type,
                x_column=x_column,
                y_column=y_column,
                title=title,
                label=label
            )
            return bar_chart_file
            
        except Exception as e:
            return f"Failed to generate bar chart: {e}"
    
    elif graph_type == 'scatter':
        try:
            scatter_plot_file = graph_generator.create_graph_from_csv(
                file_path=file_path,
                graph_type=graph_type,
                x_column=x_column,
                y_column=y_column,
                title=title,
                label=label
            )
            return scatter_plot_file
        except Exception as e:
            return f"Failed to generate scatter plot: {e}"
            
    elif graph_type == 'line':     
        try:
            line_chart_file = graph_generator.create_graph_from_csv(
                file_path=file_path,
                graph_type=graph_type,
                x_column=x_column,
                y_column=y_column,
                title=title,
                label=label
            )
            return line_chart_file
        except Exception as e:
            return f"Failed to generate line chart: {e}"
            
    elif graph_type == 'pie':
        try:
            pie_chart_file = graph_generator.create_graph_from_csv(
                file_path=file_path,
                graph_type=graph_type,
                column=column,
                title=title
               
            )
            return pie_chart_file
        except Exception as e:
            return f"Failed to generate pie chart: {e}"
    else:
        return "Invalid graph type. Choose from: 'bar', 'scatter', 'line', 'pie'" 
    
    
 
class GraphGeneratorSchema(pydantic.BaseModel):
    file_path: str
    graph_type: str
    x_column: str
    y_column: str
    title: str
    label: str
    column: str