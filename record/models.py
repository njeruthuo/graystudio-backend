from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    name = models.CharField(max_length=200)
    number = PhoneNumberField(unique=True)  # Using PhoneNumberField
    date_joined = models.DateTimeField(auto_now_add=True)
    total_points = models.PositiveIntegerField(default=0)

    def update_total_points(self):
        """Update total points based on all records minus redeemed points."""
        earned_points = sum(record.points() for record in self.records.all())
        redeemed_points = sum(
            redemption.points_used for redemption in self.redemptions.all())
        self.total_points = (earned_points - redeemed_points) or 0
        self.save()

    def redeem_points(self, points_to_redeem):
        """Redeem points and store the transaction."""
        if points_to_redeem > self.total_points:
            raise ValueError("Not enough points to redeem")

        Redemption.objects.create(client=self, points_used=points_to_redeem)
        self.update_total_points()

    def __str__(self):
        return f"{self.name} ({self.total_points} pts)"


class Record(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='records')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def points(self):
        """Calculate points (1 point per shs10 spent) with exception handling."""
        try:
            if self.amount_paid is None:
                # print(self.amount_paid, "amount")
                return 0  # Return 0 points if no amount is paid
            return int(self.amount_paid // 10)
        except (TypeError, ValueError) as e:
            # Log the error for debugging
            print(f"Error calculating points for record {self.id}: {e}")
            return 0

    def save(self, *args, **kwargs):
        """Update client's points when a record is saved."""
        super().save(*args, **kwargs)
        self.client.update_total_points()

    def __str__(self):
        return f"{self.client.name} - {self.amount_paid} on {self.date}"


class Redemption(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='redemptions')
    points_used = models.PositiveIntegerField()
    date_redeemed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} redeemed {self.points_used} points on {self.date_redeemed}"
