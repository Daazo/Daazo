import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import discord

class CaptchaGenerator:
    """Generate CAPTCHA images with random text and distortions"""
    
    def __init__(self):
        self.width = 300
        self.height = 100
        self.char_length = 6
        
    def generate_text(self):
        """Generate random CAPTCHA text (alphanumeric, no ambiguous characters)"""
        # Exclude confusing characters: 0, O, I, l, 1
        chars = ''.join([c for c in string.ascii_uppercase + string.digits if c not in 'O0Il1'])
        return ''.join(random.choice(chars) for _ in range(self.char_length))
    
    def create_captcha(self, text):
        """Create CAPTCHA image with text"""
        # Create base image
        image = Image.new('RGB', (self.width, self.height), color=(20, 20, 40))
        draw = ImageDraw.Draw(image)
        
        # Add noise lines
        for _ in range(8):
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            x2 = random.randint(0, self.width)
            y2 = random.randint(0, self.height)
            draw.line([(x1, y1), (x2, y2)], fill=(138, 79, 255), width=2)
        
        # Add noise dots
        for _ in range(100):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.point((x, y), fill=(random.randint(100, 200), random.randint(100, 200), random.randint(100, 255)))
        
        # Try to load a font, fallback to default if not available
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 48)
            except:
                font = ImageFont.load_default()
        
        # Calculate text position to center it
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2
        
        # Draw each character with random colors and slight offsets
        char_x = x
        for char in text:
            # Random color for each character (purple/blue theme)
            color = (
                random.randint(138, 200),  # R
                random.randint(79, 150),   # G
                random.randint(200, 255)   # B
            )
            
            # Random vertical offset
            char_y = y + random.randint(-5, 5)
            
            # Draw character
            draw.text((char_x, char_y), char, font=font, fill=color)
            
            # Get character width for next position
            char_bbox = draw.textbbox((0, 0), char, font=font)
            char_width = char_bbox[2] - char_bbox[0]
            char_x += char_width + random.randint(-2, 2)
        
        # Apply slight blur
        image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Add border
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0, 0), (self.width-1, self.height-1)], outline=(138, 79, 255), width=3)
        
        return image
    
    def get_captcha_file(self, text):
        """Convert CAPTCHA image to Discord file"""
        image = self.create_captcha(text)
        
        # Save to bytes buffer
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Create Discord file
        return discord.File(buffer, filename='captcha.png')
    
    def generate(self):
        """Generate complete CAPTCHA (text + image file)"""
        text = self.generate_text()
        file = self.get_captcha_file(text)
        return text, file
