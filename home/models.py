from django.db import models

# Create your models here.
class Chef(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Cuisine(models.Model):
    name = models.CharField(max_length=100)
    chefs = models.ForeignKey(Chef, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
class Dish(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/')
    description = models.TextField()
    price = models.FloatField()
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    avaibility = models.BooleanField(default=True)
    cooking_time = models.CharField(max_length=100, default='10 min')

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    table_number = models.IntegerField()
    persons = models.IntegerField()

    def __str__(self):
        return f"{self.name} - Table {self.table_number}"
    
class Order(models.Model):
    dishes = models.ManyToManyField(Dish, through='OrderItem')
    order_time = models.DateTimeField(auto_now_add=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id} by {self.customer_id.name} - Table {self.customer_id.table_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.dish.name}"
    

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for order {self.order.id}"
