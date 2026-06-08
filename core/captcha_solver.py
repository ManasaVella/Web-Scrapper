import time
import requests

class AntiBotBypass:
    def __init__(self, validation_token):
        self.auth_token = validation_token
        self.gateway_inbound = "http://2captcha.com/in.php"
        self.gateway_outbound = "http://2captcha.com/res.php"

    def execute_bypass(self, form_site_key, target_domain):
        """Dispatches data payloads to 2Captcha workers and polls for the solved token."""
        if not self.auth_token:
            print("❌ Bypass process aborted: Missing developer validation credentials.")
            return None

        form_data = {
            'key': self.auth_token,
            'method': 'userrecaptcha',
            'googlekey': form_site_key,
            'pageurl': target_domain,
            'json': 1
        }
        
        try:
            print("🧩 Transmitting challenge token details to external solver array...")
            api_reply = requests.post(self.gateway_inbound, data=form_data, timeout=15).json()
            
            if api_reply.get("status") != 1:
                print(f"❌ Verification platform rejected request parameters: {api_reply.get('request')}")
                return None
                
            session_job_id = api_reply.get("request")
            print(f"✅ Challenge logged. Job ID assigned: {session_job_id}. Polling worker queue...")
            
            time.sleep(25)  # Slightly longer introductory wait to shift processing patterns
            for check_cycle in range(12):
                print(f"⏳ Verification status poll (Request attempt {check_cycle + 1})...")
                query_string = {
                    'key': self.auth_token,
                    'action': 'get',
                    'id': session_job_id,
                    'json': 1
                }
                
                downloaded_result = requests.get(self.gateway_outbound, params=query_string, timeout=12).json()
                if downloaded_result.get("status") == 1:
                    print("🎉 Verification sequence completely bypassed successfully!")
                    return downloaded_result.get("request")
                    
                if downloaded_result.get("request") == "CAPCHA_NOT_READY":
                    time.sleep(6)
                else:
                    print(f"❌ Solver execution error flag encountered: {downloaded_result.get('request')}")
                    return None
                    
        except Exception as error_context:
            print(f"❌ Structural crash handled in verification thread framework: {error_context}")
            
        return None