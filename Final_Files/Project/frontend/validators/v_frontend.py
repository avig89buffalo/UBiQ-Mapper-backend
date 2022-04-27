from werkzeug.exceptions import HTTPException

class FrontendValidator:
    @staticmethod
    def order_lat_and_long(lat1,lat2,long1,long2):
        if lat1>lat2:
            temp=lat1
            lat1=lat2
            lat2=temp
        if long1>long2:
            temp=long1
            long1=long2
            long2=temp   
        return lat1,lat2,long1,long2
    
    @staticmethod
    def check_lat(lat):
        if(lat>90 or lat<-90):
            raise HTTPException(400,'Invalid Parameters')
        
    @staticmethod
    def check_long(long):
        if(long>180 or long<-180):
            raise HTTPException(400,'Invalid Parameters')
        
    @staticmethod
    def validate_bounding_box(lat1,lat2,long1,long2):
        try:
            FrontendValidator.check_lat(float(lat1))
            FrontendValidator.check_lat(float(lat2))
            FrontendValidator.check_long(float(long1))
            FrontendValidator.check_long(float(long2))
        except:
            raise HTTPException(400,'Invalid Parameters')
        return FrontendValidator.order_lat_and_long(lat1,lat2,long1,long2)
    
    
 
    