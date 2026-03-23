from PIL import Image, ImageDraw, ImageFont

def create_form(candidate_name, vote_count, filename):
    # Create a white "paper"
    img = Image.new('RGB', (500, 300), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    d.text((10, 50), f"Polling Station: PS-002", fill=(0,0,0))
    d.text((10, 100), "----------------------------", fill=(0,0,0))
    
    d.text((10, 150), f"{candidate_name} : {vote_count}", fill=(0,0,0))
    
    img.save(filename)
    print(f"✅ Created {filename}")

# Generate a few test forms
create_form("Candidate A", "300", "form_station_01.png")
create_form("Candidate B", "320", "form_station_02.png")