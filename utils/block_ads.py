
'''
攔截論壇廣告 
'''

class BlockAds:
# 定義要封鎖的資源類型
    BLOCKED_TYPES = {"image", "font", "media", "stylesheet"}
    
    # 定義廣告商網域黑名單
    AD_DOMAINS = ["google-analytics.com", "doubleclick.net", "adsystem.com"]
    @classmethod
    def apply_extreme_filter(cls, route):
        """
        極速過濾模式：只留 HTML 和 XHR (API) 請求
        """
        req = route.request
        
        # 1. 根據資源類型攔截
        if req.resource_type in cls.BLOCKED_TYPES:
            return route.abort()
            
        # 2. 根據 URL 關鍵字攔截
        if any(domain in req.url for domain in cls.AD_DOMAINS):
            return route.abort()

        # 3. 其他通訊則放行
        return route.continue_()