from django.db import models
import datetime

class Product(models.Model):
    name = models.CharField(max_length=255)
    weight = models.IntegerField()
    demand_percent = models.FloatField()

    def __str__(self):
        return self.name

class ShelfAllocation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shelf = models.IntegerField()
    column = models.IntegerField()
    
    def __str__(self):
        return f"{self.product.name} -> Shelf {self.shelf}, Column {self.column}"

class OptimizationResult(models.Model):
    METHOD_CHOICES = [
        ('harmony', 'Harmony Search'),
        ('tabu', 'Tabu Search'),
    ]

    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    fitness_score = models.IntegerField()
    time_taken = models.FloatField(help_text="Time in seconds", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    penalty_log = models.TextField()  # Store as plain text

    def __str__(self):
        return f"{self.get_method_display()} - Fitness: {self.fitness_score}"
