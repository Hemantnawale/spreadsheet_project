from django.shortcuts import render
from django.http import HttpResponse
import copy

def index(request):
    # Initialize a blank spreadsheet (10x10 grid) if not provided
    if request.method == "POST":
        data = request.POST.getlist('cell')
        operation = request.POST.get('operation')
        range_str = request.POST.get('range')
        find_text = request.POST.get('find', '')
        replace_text = request.POST.get('replace', '')

        # Convert flat list to 10x10 grid
        grid = [data[i:i+10] for i in range(0, len(data), 10)]
        original_grid = copy.deepcopy(grid)  # Keep a copy for operations

        # Parse range
        try:
            start, end = range_str.split(':')
            start_row, start_col = int(start[1:]) - 1, ord(start[0].upper()) - 65
            end_row, end_col = int(end[1:]) - 1, ord(end[0].upper()) - 65
        except ValueError:
            return render(request, 'spreadsheet_app/index.html', {'grid': grid, 'error': 'Invalid range'})

        # Perform operation
        if operation == "SUM":
            values = [
                float(grid[row][col])
                for row in range(start_row, end_row + 1)
                for col in range(start_col, end_col + 1)
                if grid[row][col]
            ]
            result = sum(values)

        elif operation == "COUNT":
            values = [
                grid[row][col]
                for row in range(start_row, end_row + 1)
                for col in range(start_col, end_col + 1)
                if grid[row][col]
            ]
            result = len(values)
            
        elif operation == "MIN":
            values = [
                float(grid[row][col])
                for row in range(start_row, end_row + 1)
                for col in range(start_col, end_col + 1)
                if grid[row][col]
            ]
            result = min(values) if values else None
            
        elif operation == "MAX":
            values = [
                float(grid[row][col])
                for row in range(start_row, end_row + 1)
                for col in range(start_col, end_col + 1)
                if grid[row][col]
            ]
            result = max(values) if values else None

        elif operation == "AVG":
            values = [
                float(grid[row][col])
                for row in range(start_row, end_row + 1)
                for col in range(start_col, end_col + 1)
                if grid[row][col]
            ]
            result = sum(values) / len(values) if values else 0

        elif operation == "TRIM":
            for row in range(len(grid)):
                for col in range(len(grid[row])):
                    grid[row][col] = grid[row][col].strip() 
                    # if grid[row][col] else grid[row][col]
                    print(grid[row][col])
            result = None

        elif operation == "UPPER":
            for row in range(len(grid)):
                for col in range(len(grid[row])):
                    grid[row][col] = grid[row][col].upper()
                    print(grid[row][col])
            result = None

        elif operation == "LOWER":
            for row in range(len(grid)):
                for col in range(len(grid[row])):
                    grid[row][col] = grid[row][col].lower()
                    print(grid[row][col])
            result = None

        elif operation == "REMOVE_DUPLICATES":
            seen = set()
            for row in range(len(grid)):
                for col in range(len(grid[row])):
                    if grid[row][col] in seen:
                        grid[row][col] = ""
                    else:
                        seen.add(grid[row][col])
            result = None

        elif operation == "FIND_REPLACE":
            for row in range(len(grid)):
                for col in range(len(grid[row])):
                    if grid[row][col] and find_text in grid[row][col]:
                        grid[row][col] = grid[row][col].replace(find_text, replace_text)
            result = None
        else:
            result = None

        return render(request, 'spreadsheet_app/index.html', {'grid': grid, 'result': result})

    # Default: Empty grid
    grid = [["" for _ in range(10)] for _ in range(10)]
    
    return render(request, 'spreadsheet_app/index.html', {'grid': grid})
