import re


class OrderExtractor:
    """
    Regex-based NLP engine for extracting order details from Vietnamese text.
    
    Automatically detects:
    - Phone numbers (Vietnamese mobile format: 03x, 05x, 07x, 08x, 09x + 8 digits)
    - Delivery addresses (districts, provinces, streets)
    - Product variants (colors, sizes, quantities)
    - Purchase intentions (keywords like "mua", "chốt", "lấy")
    
    Attributes:
        phone_pattern (regex): Compiled pattern for Vietnamese mobile numbers
        buy_keywords (list): Words indicating purchase intention
        address_keywords (list): Location-related keywords
        provinces (list): Vietnamese province names for better matching
    """
    
    def __init__(self):
        """Initialize OrderExtractor with Vietnamese-specific patterns and keywords."""
        # Vietnamese phone number regex (03, 05, 07, 08, 09) + 8 digits
        self.phone_pattern = re.compile(r'(0[3|5|7|8|9])+([0-9]{8})\b')
        
        # Keywords indicating a purchase intention
        self.buy_keywords = [
            'chốt', 'lấy', 'mua', 'ship', 'đặt', 'giao', 
            'mình 1', 'cho em', 'tớ lấy', 'giữ cho'
        ]
        
        # Basic address structural keywords to hint at location 
        self.address_keywords = [
            'quận', 'huyện', 'phường', 'xã', 'đường', 'thành phố', 
            'tp', 'tòa nhà', 'ngõ', 'ngách', 'hẻm', 'số nhà', 'tỉnh'
        ]
        
        # Major Vietnam provinces for better matching
        self.provinces = [
            'hà nội', 'hồ chí minh', 'hcm', 'đà nẵng', 'hải phòng', 
            'cần thơ', 'bình dương', 'đồng nai', 'quảng ninh', 'thanh hóa', 
            'nghệ an', 'huế', 'bắc ninh'
        ]

    def extract(self, text):
        """
        Extract order-related information from unstructured Vietnamese text.
        
        Extraction logic:
        1. Search for phone numbers in Vietnamese operator format
        2. Check for purchase intention keywords
        3. Find address hints using location keywords and province names
        4. Identify product variants (sizes, colors, quantities)
        5. Classify as "order" if phone exists OR (buy intent + address exists)
        
        Args:
            text (str): Vietnamese text to extract order information from
            
        Returns:
            dict: Contains:
                - 'is_order' (bool): Whether text likely contains an order
                - 'phone' (str): Extracted phone number (empty if not found)
                - 'address_hint' (str): Inferred delivery address
                - 'product_hint' (str): Product variant information
        """
        text_lower = text.lower()
        
        # 1. Extract Phone Number
        phone_match = self.phone_pattern.search(text)
        phone = phone_match.group(0) if phone_match else ""
        
        # 2. Check for Purchase Intention
        has_buy_intent = any(kw in text_lower for kw in self.buy_keywords)
        
        # If no phone and no clear intent, probably not an order
        if not phone and not has_buy_intent:
            return {
                'is_order': False,
                'phone': "",
                'address_hint': "",
                'product_hint': ""
            }

        # 3. Extract Address Hints (Look for text fragments containing address keywords or provinces)
        address_hint = ""
        # Split text by commas or dots to find the segment with address info
        segments = re.split(r'[,.\n\-]+', text)
        address_segments = []
        for segment in segments:
            seg_lower = segment.lower()
            if any(akw in seg_lower for akw in self.address_keywords) or any(
                pr in seg_lower for pr in self.provinces
            ):
                address_segments.append(segment.strip())
        
        if address_segments:
            address_hint = ", ".join(address_segments)

        # 4. Extract Product/Variant Hints (Look for specific units of measurement or variation terms)
        product_hint = ""
        variant_keywords = ['size', 'màu', 'ly', 'cốc', 'chiếc', 'cái', 'túi', 'bé', 'sz', 'kg', 'ký']
        for segment in segments:
            if any(vkw in segment.lower().split() for vkw in variant_keywords):
                product_hint += segment.strip() + " "
        
        product_hint = product_hint.strip()
        
        # Fallback: if no specific product hint found, grab words immediately after buy keyword
        if not product_hint and has_buy_intent:
            match = re.search(r'(chốt|lấy|mua)(.*?)(0[3|5|7|8|9]|$)', text_lower)
            if match and match.group(2).strip():
                # limit length and clean up trailing characters
                product_hint = match.group(2).strip()[:40].strip(',.- ')
        
        # It's highly likely an order if there's a phone number OR (explicit buy intent + address)
        is_order = bool(phone) or (has_buy_intent and bool(address_hint))

        return {
            'is_order': is_order,
            'phone': phone,
            'address_hint': address_hint,
            'product_hint': product_hint.title() if product_hint else "Không rõ"
        }


# Singleton instance for use throughout the app
order_extractor = OrderExtractor()
