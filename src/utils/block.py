from src.utils.common import load_ymal
from src.config import CONFIG_DEFAULT


config = load_ymal(CONFIG_DEFAULT)

def apply_extreme_filter(route):
    """
    過濾邏輯:過濾完後差不多只留 HTML 和 XHR (API) 請求
    """
    req = route.request
    
    # 1. 根據資源類型攔截
    if req.resource_type in config['block_setting']['blocked_types']:
        return route.abort()
        
    # 2. 根據 URL 關鍵字攔截
    if any(domain in req.url for domain in config['block_setting']['ad_domains']):
        return route.abort()

    # 3. 其他通訊則放行
    return route.continue_()

