import math
import growth_data
import growth_data_extended
from datetime import datetime

class AnalysisService:
    @staticmethod
    def format_yas(year, month):
        return f"{int(year)} Yıl {int(month)} Ay"

    @staticmethod
    def calculate_lms(value, l, m, s):
        """
        Calculate Z-score using LMS method:
        Z = ((observed / M) ** L - 1) / (L * S)  if L != 0
        Z = ln(observed / M) / S                 if L == 0
        """
        if l == 0:
            z = math.log(value / m) / s
        else:
            z = ((value / m) ** l - 1) / (l * s)
        
        # Calculate Percentile from Z
        percentile = 0.5 * (1 + math.erf(z / math.sqrt(2))) * 100
        return z, percentile

    @staticmethod
    def get_lms_params(gender, metric, months):
        try:
            # growth_data.LMS_DATA keys are integers (months)
            data_source = growth_data.LMS_DATA[gender][metric]
            
            # 10-19 yaş kilo verisi kontrolü
            if metric == 'kilo' and months > 120:
                if gender in growth_data_extended.LMS_DATA_EXTENDED:
                    # Genişletilmiş veriye geçiş yapıyoruz ama interpolasyon için 120. ayı da kapsayabiliriz
                    data_source = growth_data_extended.LMS_DATA_EXTENDED[gender][metric]
            
            data = data_source
            keys = sorted(data.keys())
            
            # Clamp
            if months <= keys[0]: months = keys[0]
            if months >= keys[-1]: months = keys[-1]
            
            # Interpolation
            for i in range(len(keys)-1):
                if keys[i] <= months <= keys[i+1]:
                    t1, t2 = keys[i], keys[i+1]
                    vals1 = data[t1]
                    vals2 = data[t2]
                    
                    ratio = (months - t1) / (t2 - t1)
                    l = vals1[0] + (vals2[0] - vals1[0]) * ratio
                    m = vals1[1] + (vals2[1] - vals1[1]) * ratio
                    s = vals1[2] + (vals2[2] - vals1[2]) * ratio
                    return l, m, s
            return data[months] # Fallback
        except KeyError:
             return None

    @staticmethod
    def perform_analysis(gun, ay, yil, k_gun, k_ay, k_yil, boy, kilo, cinsiyet):
        try:
            if boy <= 0 or kilo <= 0: return {"error": "Boy ve kilo pozitif olmalı."}
            
            dogum_tarihi = datetime(yil, ay, gun)
            kontrol_tarihi = datetime(k_yil, k_ay, k_gun)
            
            if kontrol_tarihi < dogum_tarihi:
                 return {"error": "Kontrol tarihi doğum tarihinden önce olamaz."}

            yas_gun = (kontrol_tarihi - dogum_tarihi).days
            yas_ay_total = yas_gun / 30.4375 
            yas_yil = yas_gun / 365.25
            yas_str = AnalysisService.format_yas(yas_yil, yas_ay_total % 12)
            
            warning = None
            if yas_yil > 19:
                warning = "Bu program 0-19 yaş arası çocuklar içindir."
            
            results = {
                "yas_str": yas_str,
                "yas_ay_total": yas_ay_total,
                "warning": warning,
                "bmi": {},
                "kilo": {},
                "boy": {}
            }

            # --- Boy ---
            lms_boy = AnalysisService.get_lms_params(cinsiyet, 'boy', yas_ay_total)
            if lms_boy:
                boy_z, boy_p = AnalysisService.calculate_lms(boy, *lms_boy)
                results["boy"] = {"val": boy, "z": boy_z, "p": boy_p}
            
            # --- Kilo ---
            # WHO allows Weight up to 10y (120m). 
            # Extended with CPEG/CDC data up to 19y (228m).
            lms_kilo = AnalysisService.get_lms_params(cinsiyet, 'kilo', yas_ay_total)
            if lms_kilo and yas_ay_total <= 229: 
                kilo_z, kilo_p = AnalysisService.calculate_lms(kilo, *lms_kilo)
                results["kilo"] = {"val": kilo, "z": kilo_z, "p": kilo_p}

            # --- BMI ---
            bmi = kilo / ((boy / 100) ** 2)
            lms_bmi = AnalysisService.get_lms_params(cinsiyet, 'bmi', yas_ay_total)
            if lms_bmi:
                bmi_z, bmi_p = AnalysisService.calculate_lms(bmi, *lms_bmi)
                bmi_yorum = "Normal"
                if bmi_p < 5: bmi_yorum = "Zayıf (Underweight)"
                elif 5 <= bmi_p < 85: bmi_yorum = "Sağlıklı (Healthy)"
                elif 85 <= bmi_p < 95: bmi_yorum = "Fazla Kilolu (Overweight)"
                elif bmi_p >= 95: bmi_yorum = "Obez (Obese)"
                
                results["bmi"] = {"val": bmi, "z": bmi_z, "p": bmi_p, "yorum": bmi_yorum}

            return results

        except Exception as e:
            return {"error": str(e)}
