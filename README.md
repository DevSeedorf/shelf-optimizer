# Shelf Optimizer

A Django-based warehouse shelf optimization system that uses metaheuristic algorithms to optimize product placement on shelves based on demand patterns and weight constraints.

## 🎯 Overview

The Shelf Optimizer is designed to solve the warehouse shelf allocation problem by intelligently placing products on shelves to minimize penalties and maximize efficiency. The system uses two optimization algorithms:

- **Harmony Search Algorithm**: A music-inspired metaheuristic optimization technique
- **Tabu Search Algorithm**: A local search metaheuristic that uses memory structures

## ✨ Features

- **Product Management**: Add, view, and delete products with weight and demand specifications
- **Intelligent Shelf Allocation**: Automatically optimize product placement using advanced algorithms
- **Multiple Optimization Methods**: Choose between Harmony Search and Tabu Search algorithms
- **Real-time Performance Tracking**: Monitor optimization results and execution times
- **Historical Analysis**: View and manage optimization history
- **Penalty System**: Built-in rules for demand-based shelf placement

## 🏗️ System Architecture

### Models

1. **Product**: Stores product information (name, weight, demand percentage)
2. **ShelfAllocation**: Records product placement (product, shelf, column)
3. **OptimizationResult**: Tracks optimization runs (method, fitness score, execution time, penalty log)

### Constraints

- **7 Shelves × 7 Columns** warehouse layout
- **Weight Limits**: 10,000 - 25,000 kg per shelf
- **Demand-Based Placement Rules**:
  - High demand (>90%): Shelves 3-5
  - Average demand (60-80%): Shelves 1-2  
  - Low demand (<60%): Shelves 6-7

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Django 5.1.7
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DevSeedorf/Shelf-Allocation-and-Space-Optimization-Using-Harmony-and-Tabu-Search-Algorithm.git
   cd shelf
   ```

2. **Create and activate virtual environment**
   ```powershell
   python -m venv virt
   virt\Scripts\activate
   ```

3. **Install dependencies**
   ```powershell
   pip install django
   ```

4. **Navigate to project directory**
   ```powershell
   cd shelf_optimizer
   ```

5. **Run migrations**
   ```powershell
   python manage.py migrate
   ```

6. **Start the development server**
   ```powershell
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000/`

## 📋 Usage

### Adding Products

1. Navigate to the product list page
2. Click "Add Product" 
3. Enter product details:
   - **Name**: Product identifier
   - **Weight**: Product weight in kg
   - **Demand Percent**: Demand percentage (0-100)

### Running Optimization

1. Go to the shelf allocation page
2. Choose optimization method:
   - **Harmony Search**: For exploration-focused optimization
   - **Tabu Search**: For exploitation-focused optimization
3. View results including:
   - Fitness score (lower is better)
   - Execution time
   - Penalty breakdown
   - Final shelf allocation

### Viewing History

- Access optimization history to track performance over time
- Compare different algorithm results
- Clear history when needed

## 🔧 Algorithm Details

### Harmony Search Parameters

- **HMCR (Harmony Memory Considering Rate)**: 0.8
- **PAR (Pitch Adjusting Rate)**: 0.4
- **HMS (Harmony Memory Size)**: 50
- **NI (Number of Iterations)**: 50

### Fitness Function

The fitness function calculates penalties based on:
- Demand-based shelf placement violations
- Weight constraint violations
- Product type grouping (optional)

Lower fitness scores indicate better solutions.

## 📊 Performance Metrics

The system tracks:
- **Fitness Score**: Total penalty points
- **Execution Time**: Algorithm runtime in seconds
- **Penalty Log**: Detailed violation breakdown
- **Historical Trends**: Performance over multiple runs

## 🗂️ Project Structure

```
shelf_optimizer/
├── manage.py                 # Django management script
├── db.sqlite3               # SQLite database
├── shelf_optimizer/         # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── products/                # Core application
    ├── models.py           # Data models
    ├── views.py            # View logic
    ├── optimizer.py        # Optimization algorithms
    ├── forms.py            # Django forms
    ├── admin.py            # Admin interface
    ├── templates/          # HTML templates
    └── migrations/         # Database migrations
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔮 Future Enhancements

- [ ] Advanced visualization of shelf layouts
- [ ] Additional optimization algorithms (Genetic Algorithm, Simulated Annealing)
- [ ] Real-time optimization monitoring
- [ ] Export/import functionality for product data
- [ ] RESTful API for external integrations
- [ ] Multi-warehouse support
- [ ] Advanced reporting and analytics

## 📞 Support

For questions, issues, or contributions, please:
1. Check the existing issues on GitHub
2. Create a new issue with detailed description
3. Contact the development team

---

**Built with ❤️ using Django and Python**
