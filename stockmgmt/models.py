from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.FloatField(help_text="Quantity (liters/kg)")
    stock = models.FloatField(help_text="Quantity in Stock (liters/kg)")
    sold = models.FloatField(help_text="Quantity Sold (liters/kg)")
    production_date = models.DateField()
    expiration_date = models.DateField()
    min_stock = models.FloatField(help_text="Minimum Stock Threshold (liters/kg)")
    reorder_qty = models.FloatField(help_text="Reorder Quantity (liters/kg)")
    abc_class = models.CharField(max_length=20, blank=True)
    stock_urgency = models.CharField(max_length=20, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    prediction = models.BooleanField(default=False)
    confidence = models.FloatField(null=True)
    last_predicted = models.DateTimeField(auto_now=True)

    def stock_status(self):
        if self.prediction:
            return "Above Threshold"
        return "Below Threshold"

    def confidence_percentage(self):
        return f"{self.confidence * 100:.1f}%" if self.confidence else "N/A"

    def __str__(self):
        return self.name


class StockPrediction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    prediction_date = models.DateTimeField(auto_now_add=True)
    predicted_sales = models.FloatField()
    recommendation = models.TextField()
    confidence = models.FloatField(null=True, blank=True)