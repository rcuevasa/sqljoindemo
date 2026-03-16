import sqlite3
import os
import sys
from contextlib import contextmanager
from typing import List, Dict, Any
import shutil
import json

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect('joins_demo.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def get_terminal_width():
    """Get terminal width, capped at 80"""
    try:
        width = shutil.get_terminal_size().columns
        return min(width, 80)
    except:
        return 80

def get_terminal_height():
    """Get terminal height"""
    try:
        return shutil.get_terminal_size().lines
    except:
        return 24

def wrap_text(text: str, width: int = None) -> str:
    """Wrap text to fit within specified width"""
    if width is None:
        width = get_terminal_width()
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    for word in words:
        word_len = len(word)
        if current_length + word_len + (1 if current_line else 0) <= width:
            current_line.append(word)
            current_length += word_len + (1 if len(current_line) > 1 else 0)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = word_len
    if current_line:
        lines.append(' '.join(current_line))
    return '\n'.join(lines)

def print_table(headers: List[str], rows: List[List[Any]]):
    """Print data in SQLite .mode table format with box-drawing characters"""
    if not rows:
        print("(empty)")
        return

    # Calculate column widths
    col_widths = []
    for col_idx in range(len(headers)):
        max_width = len(str(headers[col_idx]))
        for row in rows:
            max_width = max(max_width, len(str(row[col_idx])))
        col_widths.append(max_width + 1)  # Add 1 for padding

    # Create horizontal borders
    top = '┌' + '┬'.join('─' * w for w in col_widths) + '┐'
    middle = '├' + '┼'.join('─' * w for w in col_widths) + '┤'
    bottom = '└' + '┴'.join('─' * w for w in col_widths) + '┘'

    # Print table
    print(top)
    # Print header
    header_line = '│' + ''.join(f' {str(h).ljust(w-1)}│' for h, w in zip(headers, col_widths))
    print(header_line)
    print(middle)
    # Print data rows
    for row in rows:
        row_line = '│' + ''.join(f' {str(v).ljust(w-1)}│' for v, w in zip(row, col_widths))
        print(row_line)
    print(bottom)

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

# Global state for query visibility
show_query = True

def wait_for_keypress(prompt="Press Enter to continue (q to quit)...\n"):
    """Wait for user to press a key, return 'quit' if q or escape was pressed, 'toggle' if v was pressed, 'next' if Enter was pressed"""
    global show_query
    print(prompt, end='', flush=True)
    try:
        import termios
        import tty
        def getch():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
        ch = getch()
        if ch.lower() == 'v':
            # Toggle query visibility
            show_query = not show_query
            return 'toggle'
        if ch.lower() == 'q' or ch == '\x1b':
            return 'quit'
        return 'next'
    except Exception:
        try:
            user_input = input()
            if user_input.lower() == 'v':
                show_query = not show_query
                return 'toggle'
            if user_input.lower() == 'q':
                return 'quit'
            return 'next'
        except (EOFError, KeyboardInterrupt):
            return 'quit'

def print_separator(char='=', length=60):
    """Print a separator line"""
    width = get_terminal_width()
    print(char * width)

def format_sql_query(query: str) -> str:
    """Format SQL query with indentation for better readability"""
    lines = query.strip().split('\n')
    # Remove extra indentation
    formatted_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            # Keep keywords like SELECT, FROM, WHERE, etc. at their own line
            # and indent rest
            if any(keyword in stripped.upper() for keyword in ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'HAVING', 'UNION', 'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'FULL JOIN', 'CROSS JOIN', 'LEFT', 'RIGHT', 'INNER', 'CROSS']):
                formatted_lines.append('    ' + stripped)
            else:
                # Indent continuation lines
                formatted_lines.append('        ' + stripped)
    return '\n'.join(formatted_lines)

def print_query_result(query: str, description: str = ""):
    """Execute query and display results with formatting"""
    width = get_terminal_width()
    if description:
        print(wrap_text(description, width))
    
    # Show query based on global state
    if show_query:
        print("Query:")
        print(format_sql_query(query))
    else:
        print("[Press 'v' to view SQL query]")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            headers = list(rows[0].keys())
            data = [list(row) for row in rows]
            print_table(headers, data)
            print(f"Total rows: {len(rows)}")
        else:
            print("(empty)")

def demonstrate_join(title: str, description: str, query: str, result_title: str):
    """Generic demonstration function that shows a join operation"""
    width = get_terminal_width()
    print("="*width)
    print(title)
    print("="*width)
    print(wrap_text(description, width))
    print_query_result(query, result_title)

def load_demo_config() -> list:
    """Load demonstration configurations from JSON file"""
    try:
        with open('demo_config.json', 'r') as f:
            config = json.load(f)
            return config.get('demonstrations', [])
    except Exception as e:
        print(f"Error loading demo configuration: {e}")
        return []

def print_intro():
    """Print formatted introduction page"""
    width = get_terminal_width()
    height = get_terminal_height()
    
    print("="*width)
    print("SQL JOINS DEMONSTRATION")
    print("="*width)
    print()
    
    # Check if we have enough height for detailed formatting
    use_detailed = height >= 20
    
    if use_detailed:
        # Detailed formatting with sections
        print("BASIC JOINs:")
        print("-" * width)
        print("  INNER JOIN          : Only matching rows")
        print("  LEFT JOIN           : All from left, matching from right")
        print("  LEFT JOIN (no NULLs): LEFT JOIN with WHERE filtering NULLs")
        print("  RIGHT JOIN          : All from right, matching from left")
        print("  FULL OUTER          : All from both tables")
        print()
        print("ADVANCED JOINs:")
        print("-" * width)
        print("  SELF JOIN           : Join a table to itself")
        print("  CROSS JOIN          : Cartesian product")
        print("  ANTI-JOIN (A)      : Find records NOT matching")
        print("  ANTI-JOIN (B)      : Find orphan records")
        print("  JOIN + AGGREGATION (A): Order summary with COUNT, SUM, AVG")
        print("  JOIN + AGGREGATION (B): Product statistics with COUNT")
        print("  MULTIPLE JOINS      : Join 3+ tables")
        print("  NON-EQUI JOIN (A)   : Join with > comparison")
        print("  NON-EQUI JOIN (B)   : Join with BETWEEN range")
        print()
        print("SAMPLE DATA:")
        print("-" * width)
        print("  Users  : Alice, Bob, Charlie (has 3 orders), Diana, Eve (no orders)")
        print("  Orders : 7 total (1 orphan order with user_id=99)")
        print("  Employees: 7 employees with manager hierarchy")
        print("  Products: 3 products (Widget A, B, C)")
    else:
        # Compact formatting for smaller terminals
        intro_text = "BASIC: INNER, LEFT, LEFT(no NULLs), RIGHT, FULL OUTER. ADVANCED: SELF, CROSS, ANTI-JOIN(A+B), JOIN+AGGREGATION(A+B), MULTIPLE, NON-EQUI(A+B). DATA: 5 users, 7 orders, 7 employees, 3 products"
        print(wrap_text(intro_text, width))
        print()
        print(wrap_text("Users: Alice, Bob, Charlie (3 orders), Diana, Eve (no orders). Orders: 7 total (1 orphan, user_id=99)", width))
    
    print()

def demonstrate_comparison():
    """Side-by-side comparison of all join types with counts"""
    width = get_terminal_width()
    print("="*width)
    print("JOIN TYPE COMPARISON")
    print("="*width)
    
    # Load demo configurations
    demo_configs = load_demo_config()
    
    # Extract queries from config for comparison
    queries = {}
    for demo_config in demo_configs:
        # Extract join type from title
        title = demo_config['title']
        query = demo_config['query']
        queries[title] = query
    
    print("\nRow counts for each join type:")
    print_separator('-')
    with get_db_connection() as conn:
        cursor = conn.cursor()
        for join_type, query in queries.items():
            cursor.execute(query)
            count = len(cursor.fetchall())
            print(f"{join_type:40} : {count} rows")
    print()

def main():
    """Run all join demonstrations"""
    width = get_terminal_width()
    clear_screen()
    print_intro()
    result = wait_for_keypress("Press Enter to start the demonstrations (q to quit)...\n")
    if result == 'quit':
        return
    
    # Load demo configurations from JSON
    demo_configs = load_demo_config()
    
    # Run each demonstration
    for demo_config in demo_configs:
        clear_screen()
        demonstrate_join(
            title=demo_config['title'],
            description=demo_config['description'],
            query=demo_config['query'],
            result_title=demo_config['result_title']
        )
        
        # Handle key presses including toggle
        while True:
            result = wait_for_keypress(f"Press Enter to continue (q to quit, 'v' to {'hide' if show_query else 'show'} SQL query)...\n")
            if result == 'quit':
                return
            elif result == 'toggle':
                # Re-run current demo without clearing screen
                clear_screen()
                demonstrate_join(
                    title=demo_config['title'],
                    description=demo_config['description'],
                    query=demo_config['query'],
                    result_title=demo_config['result_title']
                )
            else:
                # Press Enter, move to next demo
                break
    
    clear_screen()
    demonstrate_comparison()
    print("="*width)
    print("Demonstration complete!")
    print("="*width)

if __name__ == '__main__':
    main()
