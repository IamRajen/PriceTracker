from celery import shared_task
from .models import TrackedProduct, Product
from .crawler import HTMLParserFactory
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import time
import traceback
from datetime import datetime
from .serializers import ProductPriceSerializer

@shared_task
def track_product_price():
    try:
        print("Running track_product_price...")
        ## get the unique products from table TrackedProduct
        tracked_products_list = Product.objects.filter(trackedproduct__isnull=False).distinct()
        send_email_list = {}

        print('--------------------------------')
        print(f'Fetching product details for {len(tracked_products_list)} products')
        changed_products_price = []
        for product in tracked_products_list:
            ## collect product price from flipkart
            html_parser = HTMLParserFactory.get_html_parser(product.source)
            product_details = html_parser.extract_product_details(product.link)
            if product_details['price'] is not None and product_details['price'] != product.price:
                if product_details['price'] < product.price:
                    send_email_list[product] = [product.price, product_details['price']]
                changed_products_price = {
                    'product': product.id,
                    'price': product_details['price'],
                    'date': datetime.now().strftime('%d/%m/%Y')
                }
                product.price = product_details['price']
                product.save()
                product_price_serializer = ProductPriceSerializer(data=changed_products_price)
                if product_price_serializer.is_valid():
                    product_price_serializer.save()
                else:
                    print(f'Error in product_price_serializer: {product_price_serializer.errors}')

            time.sleep(1)
        print('--------------------------------')
    except Exception as e:
        print(f'Error in track_product_price: {traceback.format_exc()}')
        return

    try:
        ## send the email to the user
        email_payload_per_user = {}
        for product, product_details in send_email_list.items():
            tracking_products = TrackedProduct.objects.filter(product=product.id)

            for tracking_product_item in tracking_products:
                if tracking_product_item.user.email not in email_payload_per_user:
                    email_payload_per_user[tracking_product_item.user.email] = []
                    
                email_payload_per_user[tracking_product_item.user.email].append(
                    {
                        'product_name': product.title,
                        'link': product.link,
                        'old_price': product_details[0],
                        'new_price': product_details[1]
                    }
                )

        print(f'email_payload_per_user: {email_payload_per_user}')
        for user_email, product_details in email_payload_per_user.items():
            send_email(user_email, product_details) 
    except Exception as e:
        print(f'Error in send_email: {e}')
        return

def send_email(user_email, product_details):
    try:
        print('--------------------------------')
        print(f'sending email to {user_email} for {len(product_details)} products')
        print('--------------------------------')

        email_content = ''
        for product_detail in product_details:
            email_content += f'<p><a href="{product_detail["link"]}">{product_detail["product_name"]}</a>:</p> <p>Old Price: {product_detail["old_price"]}</p> <p>New Price: {product_detail["new_price"]}</p>'
            email_content += '<br>'

        subject = "Price Drop Alert!"
        text_content = "Check out the latest price."
        html_content = f"<p><strong>Good news!</strong> The price dropped!</p>{email_content}"

        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print(f'Error in send_email: {e}')
        return

