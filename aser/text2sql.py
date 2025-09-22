import json
import sqlite3
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod


class Text2SQL:
    """Main toolkit class that combines database management and SQL generation."""

    def __init__(self, agent, db_connector, db_path):

        self.db_connector = db_connector

        self.sql_generator = SQLGenerator(agent)
        self.connected = self.db_connector.connect(db_path)

    def get_database_schema(self) -> Dict[str, Any]:
        """Get current database schema."""
        return self.db_connector.get_schema()

    def chat(self, user_query: str) -> Dict[str, Any]:
        """Generate SQL from natural language and execute it."""
        if not self.connected:
            return {
                "error": "No database connection. Please connect to a database first.",
                "sql": None,
                "results": [],
                "explanation": None
            }

        # Get schema
        schema = self.get_database_schema()
        if not schema:
            return {
                "error": "Could not retrieve database schema",
                "sql": None,
                "results": [],
                "explanation": None
            }

        # Generate SQL
        sql_result = self.sql_generator.generate_sql(user_query, schema)

        if sql_result["confidence"] == "low":
            return {
                "error": "Could not generate valid SQL query",
                "sql": sql_result.get("sql"),
                "results": [],
                "explanation": sql_result.get("explanation")
            }

        # Execute SQL
        try:
            results = self.db_connector.execute_query(sql_result["sql"])

            return {
                "error": None,
                "sql": sql_result["sql"],
                "results": results,
                "explanation": sql_result["explanation"],
                "confidence": sql_result["confidence"]
            }
        except Exception as e:
            return {
                "error": f"Error executing SQL: {str(e)}",
                "sql": sql_result["sql"],
                "results": [],
                "explanation": sql_result["explanation"]
            }

    def close_connection(self):
        """Close database connection."""
        self.db_connector.close()
        self.connected = False


class SQLGenerator:
    """Generates SQL queries from natural language using LLM."""

    def __init__(self, agent):
        self.agent = agent

    def generate_sql(self, user_query: str, schema: Dict[str, Any],
                     max_retries: int = 3) -> Dict[str, Any]:
        """Generate SQL query from natural language."""

        schema_prompt = self._format_schema_for_prompt(schema)

        system_prompt = f"""You are a SQL expert. Given a database schema and a natural language query, 
        generate the appropriate SQL statement.

        Database Schema:
        {schema_prompt}

        Rules:
        1. Only generate SELECT statements (no INSERT, UPDATE, DELETE)
        2. Use proper SQL syntax for the database type
        3. Include appropriate WHERE clauses for filtering
        4. Use JOINs when needed to connect related tables
        5. Return results in a readable format
        6. If the query is ambiguous, make reasonable assumptions
        7. Always include LIMIT clause for large result sets (default 100)

        Return your response in JSON format:
        {{
            "sql": "the generated SQL query",
            "explanation": "brief explanation of what the query does",
            "confidence": "high/medium/low confidence level"
        }}"""

        user_prompt = f"Natural language query: {user_query}"

        for attempt in range(max_retries):
            try:

                content = self.agent.chat(user_prompt, pre_messages=[
                                          {"role": "system", "content": system_prompt}])


                # Try to parse JSON response
                try:
                    result = json.loads(content)
                    if "sql" in result:
                        return result
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract SQL from the response
                    sql_match = self._extract_sql_from_text(content)
                    if sql_match:
                        return {
                            "sql": sql_match,
                            "explanation": "Generated SQL query",
                            "confidence": "medium"
                        }

                # If this is the last attempt, return a fallback
                if attempt == max_retries - 1:
                    return {
                        "sql": "SELECT 1 as error;",
                        "explanation": "Failed to generate valid SQL",
                        "confidence": "low"
                    }

            except Exception as e:

                if attempt == max_retries - 1:
                    return {
                        "sql": "SELECT 1 as error;",
                        "explanation": f"Error: {str(e)}",
                        "confidence": "low"
                    }

        return {
            "sql": "SELECT 1 as error;",
            "explanation": "Failed to generate SQL after multiple attempts",
            "confidence": "low"
        }

    def _format_schema_for_prompt(self, schema: Dict[str, Any]) -> str:
        """Format database schema for LLM prompt."""
        if not schema or "tables" not in schema:
            return "No schema information available"

        formatted_schema = f"Database Type: {schema.get('database_type', 'unknown')}\n\n"
        formatted_schema += "Tables:\n"

        for table_name, table_info in schema["tables"].items():
            formatted_schema += f"\nTable: {table_name}\n"
            formatted_schema += "Columns:\n"

            for column in table_info.get("columns", []):
                col_info = f"  - {column['name']} ({column['type']})"
                if column.get("primary_key"):
                    col_info += " [PRIMARY KEY]"
                if column.get("not_null"):
                    col_info += " [NOT NULL]"
                if column.get("default_value"):
                    col_info += f" [DEFAULT: {column['default_value']}]"
                formatted_schema += col_info + "\n"

            # Add indexes information
            if table_info.get("indexes"):
                formatted_schema += "Indexes:\n"
                for index in table_info["indexes"]:
                    formatted_schema += f"  - {index['name']}\n"

        return formatted_schema

    def _extract_sql_from_text(self, text: str) -> Optional[str]:
        """Extract SQL query from text response."""
        import re

        # Look for SQL between backticks or in code blocks
        sql_patterns = [
            r'```sql\s*(.*?)\s*```',
            r'```\s*(SELECT.*?)\s*```',
            r'`(SELECT.*?)`',
            r'(SELECT\s+.*?;)'
        ]

        for pattern in sql_patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None


class DatabaseConnector(ABC):
    """Abstract base class for database connectors."""

    @abstractmethod
    def connect(self, connection_string: str) -> bool:
        """Connect to database."""
        pass

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Get database schema information."""
        pass

    @abstractmethod
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute SQL query and return results."""
        pass

    @abstractmethod
    def close(self):
        """Close database connection."""
        pass


class SQLiteConnector(DatabaseConnector):
    """SQLite database connector."""

    def __init__(self):
        self.connection = None

    def connect(self, connection_string: str) -> bool:
        """Connect to SQLite database."""
        try:
            self.connection = sqlite3.connect(connection_string)
            self.connection.row_factory = sqlite3.Row  # Enable dict-like access
            return True
        except Exception as e:

            return False

    def get_schema(self) -> Dict[str, Any]:
        """Get SQLite database schema."""
        if not self.connection:
            return {}

        schema = {
            "tables": {},
            "database_type": "sqlite"
        }

        try:
            # Get all tables
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                schema["tables"][table_name] = {
                    "columns": [],
                    "indexes": [],
                    "foreign_keys": []
                }

                # Get column information
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()

                for col in columns:
                    column_info = {
                        "name": col[1],
                        "type": col[2],
                        "not_null": bool(col[3]),
                        "default_value": col[4],
                        "primary_key": bool(col[5])
                    }
                    schema["tables"][table_name]["columns"].append(column_info)

                # Get indexes
                cursor.execute(f"PRAGMA index_list({table_name});")
                indexes = cursor.fetchall()

                for idx in indexes:
                    index_info = {
                        "name": idx[1],
                        "unique": bool(idx[2])
                    }
                    schema["tables"][table_name]["indexes"].append(index_info)

            cursor.close()
            return schema

        except Exception as e:

            return {}

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute SQL query and return results."""
        if not self.connection:
         
            return []

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            
            # Get column names
            columns = [description[0] for description in cursor.description] if cursor.description else []
            
            # Fetch all results
            rows = cursor.fetchall()

            results = []

            for row in rows:
                result_dict = {}
                for i, value in enumerate(row):
                    result_dict[columns[i]] = value
                results.append(result_dict)

            cursor.close()
            return results

        except Exception as e:

            return []

    def close(self):
        """Close SQLite connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
