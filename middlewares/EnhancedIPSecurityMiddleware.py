from django.http import HttpResponseForbidden
from ipware import get_client_ip
from django.conf import settings
import geoip2.database
from user_agents import parse

class EnhancedIPSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.geoip_reader = geoip2.database.Reader('path/to/GeoLite2-City.mmdb')

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        current_ip, is_routable = get_client_ip(request)
        user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
        
        # Get location info
        try:
            location = self.geoip_reader.city(current_ip)
            country = location.country.iso_code
        except:
            country = None

        # Get device info
        device_info = {
            'browser': user_agent.browser.family,
            'os': user_agent.os.family,
            'device': user_agent.device.family,
            'is_mobile': user_agent.is_mobile,
            'is_tablet': user_agent.is_tablet,
            'is_pc': user_agent.is_pc
        }

        risk_score = self.calculate_risk_score(
            request.user,
            current_ip,
            country,
            device_info
        )

        if risk_score > settings.RISK_THRESHOLD:
            SuspiciousActivity.objects.create(
                user=request.user,
                previous_ip=request.user.last_login_ip,
                new_ip=current_ip,
                country=country,
                device_info=device_info,
                risk_score=risk_score
            )
            return HttpResponseForbidden("Security check failed")

        response = self.get_response(request)
        return response

    def calculate_risk_score(self, user, current_ip, country, device_info):
        score = 0
        
        # Check if IP is from a different country
        if user.last_login_country and country != user.last_login_country:
            score += 50
            
        # Check if device type changed
        if user.last_device_type and device_info['device'] != user.last_device_type:
            score += 30
            
        # Check time since last login
        time_diff = timezone.now() - user.last_login
        if time_diff.total_seconds() < 300:  # 5 minutes
            score += 20
            
        return score