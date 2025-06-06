"""
Comprehensive unit tests for WITS unit converter.

Tests all drilling industry unit conversions including:
- Drilling rates (M/HR ↔ F/HR)  
- Pressures (KPA ↔ PSI)
- Flow rates (LPM ↔ GPM)
- Mud density (KGM3 ↔ PPG)
- Temperature (°C ↔ °F)
- And more drilling-specific conversions
"""

import pytest
from models.unit_converter import UnitConverter, ConversionError
from models.unit_converter import (
    convert_drilling_rate,
    convert_pressure, 
    convert_flow_rate,
    convert_mud_density,
    convert_temperature
)
from models.symbols import WITSUnits


class TestUnitConverter:
    """Test the UnitConverter class with drilling industry units."""
    
    def test_drilling_rate_conversions(self):
        """Test drilling rate conversions (M/HR ↔ F/HR)."""
        # Metric to FPS: 30 M/HR should be ~98.43 F/HR
        result = UnitConverter.convert_value(30.0, WITSUnits.MHR, WITSUnits.FHR)
        assert abs(result - 98.4252) < 0.01
        
        # FPS to Metric: 100 F/HR should be ~30.48 M/HR  
        result = UnitConverter.convert_value(100.0, WITSUnits.FHR, WITSUnits.MHR)
        assert abs(result - 30.48) < 0.01
        
        # Test zero
        assert UnitConverter.convert_value(0.0, WITSUnits.MHR, WITSUnits.FHR) == 0.0
    
    def test_pressure_conversions(self):
        """Test pressure conversions (KPA ↔ PSI)."""
        # Metric to FPS: 1000 KPA should be ~145.04 PSI
        result = UnitConverter.convert_value(1000.0, WITSUnits.KPA, WITSUnits.PSI)
        assert abs(result - 145.038) < 0.01
        
        # FPS to Metric: 100 PSI should be ~689.48 KPA
        result = UnitConverter.convert_value(100.0, WITSUnits.PSI, WITSUnits.KPA)
        assert abs(result - 689.476) < 0.1
        
        # Test typical drilling pressures
        # 2000 PSI standpipe pressure = ~13790 KPA
        result = UnitConverter.convert_value(2000.0, WITSUnits.PSI, WITSUnits.KPA)
        assert abs(result - 13789.5) < 1.0
    
    def test_flow_rate_conversions(self):
        """Test flow rate conversions (LPM ↔ GPM)."""
        # Metric to FPS: 500 LPM should be ~132.09 GPM  
        result = UnitConverter.convert_value(500.0, WITSUnits.LPM, WITSUnits.GPM)
        assert abs(result - 132.086) < 0.01
        
        # FPS to Metric: 300 GPM should be ~1135.62 LPM
        result = UnitConverter.convert_value(300.0, WITSUnits.GPM, WITSUnits.LPM)
        assert abs(result - 1135.62) < 0.1
        
        # Test typical drilling flow rates
        # 800 GPM circulation = ~3028 LPM
        result = UnitConverter.convert_value(800.0, WITSUnits.GPM, WITSUnits.LPM)
        assert abs(result - 3028.32) < 1.0
    
    def test_mud_density_conversions(self):
        """Test mud density conversions (KGM3 ↔ PPG)."""
        # Metric to FPS: 1200 KG/M3 should be ~10.01 PPG
        result = UnitConverter.convert_value(1200.0, WITSUnits.KGM3, WITSUnits.PPG)
        assert abs(result - 10.0145) < 0.01
        
        # FPS to Metric: 9.5 PPG should be ~1138.36 KG/M3
        result = UnitConverter.convert_value(9.5, WITSUnits.PPG, WITSUnits.KGM3)
        assert abs(result - 1138.36) < 0.1
        
        # Test typical drilling mud densities
        # 12 PPG drilling mud = ~1437 KG/M3
        result = UnitConverter.convert_value(12.0, WITSUnits.PPG, WITSUnits.KGM3)
        assert abs(result - 1437.74) < 1.0
    
    def test_temperature_conversions(self):
        """Test temperature conversions (°C ↔ °F)."""
        # Celsius to Fahrenheit
        assert UnitConverter.convert_value(0.0, WITSUnits.DEGC, WITSUnits.DEGF) == 32.0
        assert UnitConverter.convert_value(100.0, WITSUnits.DEGC, WITSUnits.DEGF) == 212.0
        assert abs(UnitConverter.convert_value(37.0, WITSUnits.DEGC, WITSUnits.DEGF) - 98.6) < 0.1
        
        # Fahrenheit to Celsius  
        assert UnitConverter.convert_value(32.0, WITSUnits.DEGF, WITSUnits.DEGC) == 0.0
        assert UnitConverter.convert_value(212.0, WITSUnits.DEGF, WITSUnits.DEGC) == 100.0
        assert abs(UnitConverter.convert_value(98.6, WITSUnits.DEGF, WITSUnits.DEGC) - 37.0) < 0.1
        
        # Test typical drilling temperatures
        # 150°F bottom hole temp = ~65.56°C
        result = UnitConverter.convert_value(150.0, WITSUnits.DEGF, WITSUnits.DEGC)
        assert abs(result - 65.56) < 0.1
    
    def test_weight_force_conversions(self):
        """Test weight/force conversions (KDN ↔ KLB)."""
        # 100 KDN should be ~22.48 KLB
        result = UnitConverter.convert_value(100.0, WITSUnits.KDN, WITSUnits.KLB)
        assert abs(result - 22.4809) < 0.01
        
        # 50 KLB should be ~222.41 KDN
        result = UnitConverter.convert_value(50.0, WITSUnits.KLB, WITSUnits.KDN)
        assert abs(result - 222.41) < 0.1
    
    def test_torque_conversions(self):
        """Test torque conversions (KNM ↔ KFLB)."""
        # 10 KNM should be ~7.38 KFLB
        result = UnitConverter.convert_value(10.0, WITSUnits.KNM, WITSUnits.KFLB)
        assert abs(result - 7.37562) < 0.01
        
        # 15 KFLB should be ~20.34 KNM
        result = UnitConverter.convert_value(15.0, WITSUnits.KFLB, WITSUnits.KNM)
        assert abs(result - 20.34) < 0.1
    
    def test_length_conversions(self):
        """Test length conversions (METERS ↔ FEET)."""
        # 1000 meters should be ~3280.84 feet
        result = UnitConverter.convert_value(1000.0, WITSUnits.METERS, WITSUnits.FEET)
        assert abs(result - 3280.84) < 0.01
        
        # 5000 feet should be ~1524 meters
        result = UnitConverter.convert_value(5000.0, WITSUnits.FEET, WITSUnits.METERS)
        assert abs(result - 1524.0) < 0.1
    
    def test_same_unit_conversion(self):
        """Test that converting to the same unit returns the original value."""
        test_value = 123.45
        assert UnitConverter.convert_value(test_value, WITSUnits.PSI, WITSUnits.PSI) == test_value
        assert UnitConverter.convert_value(test_value, WITSUnits.MHR, WITSUnits.MHR) == test_value
    
    def test_unsupported_conversion(self):
        """Test that unsupported conversions raise ConversionError."""
        with pytest.raises(ConversionError):
            UnitConverter.convert_value(100.0, WITSUnits.PSI, WITSUnits.MHR)  # Pressure to rate
    
    def test_is_convertible(self):
        """Test the is_convertible method."""
        # Should be convertible
        assert UnitConverter.is_convertible(WITSUnits.KPA, WITSUnits.PSI)
        assert UnitConverter.is_convertible(WITSUnits.MHR, WITSUnits.FHR)
        assert UnitConverter.is_convertible(WITSUnits.DEGC, WITSUnits.DEGF)
        
        # Same unit should be convertible
        assert UnitConverter.is_convertible(WITSUnits.PSI, WITSUnits.PSI)
        
        # Should not be convertible
        assert not UnitConverter.is_convertible(WITSUnits.PSI, WITSUnits.MHR)
    
    def test_get_conversion_factor(self):
        """Test getting conversion factors."""
        # Should return known factors
        factor = UnitConverter.get_conversion_factor(WITSUnits.KPA, WITSUnits.PSI)
        assert abs(factor - 0.145038) < 0.000001
        
        # Should return 1.0 for same unit
        factor = UnitConverter.get_conversion_factor(WITSUnits.PSI, WITSUnits.PSI)
        assert factor == 1.0
        
        # Should return None for unsupported
        factor = UnitConverter.get_conversion_factor(WITSUnits.PSI, WITSUnits.MHR)
        assert factor is None


class TestConvenienceFunctions:
    """Test the convenience conversion functions."""
    
    def test_convert_drilling_rate(self):
        """Test drilling rate conversion function."""
        # Metric to FPS: 25 M/HR
        result = convert_drilling_rate(25.0, from_metric=True)
        assert abs(result - 82.021) < 0.1
        
        # FPS to Metric: 200 F/HR
        result = convert_drilling_rate(200.0, from_metric=False)
        assert abs(result - 60.96) < 0.1
    
    def test_convert_pressure(self):
        """Test pressure conversion function."""
        # Metric to FPS: 1500 KPA
        result = convert_pressure(1500.0, from_metric=True)
        assert abs(result - 217.557) < 0.1
        
        # FPS to Metric: 150 PSI
        result = convert_pressure(150.0, from_metric=False)
        assert abs(result - 1034.21) < 1.0
    
    def test_convert_flow_rate(self):
        """Test flow rate conversion function."""
        # Metric to FPS: 600 LPM
        result = convert_flow_rate(600.0, from_metric=True)
        assert abs(result - 158.503) < 0.1
        
        # FPS to Metric: 250 GPM
        result = convert_flow_rate(250.0, from_metric=False)
        assert abs(result - 946.35) < 1.0
    
    def test_convert_mud_density(self):
        """Test mud density conversion function."""
        # Metric to FPS: 1300 KG/M3
        result = convert_mud_density(1300.0, from_metric=True)
        assert abs(result - 10.849) < 0.01
        
        # FPS to Metric: 11 PPG
        result = convert_mud_density(11.0, from_metric=False)
        assert abs(result - 1318.12) < 1.0
    
    def test_convert_temperature(self):
        """Test temperature conversion function."""
        # Celsius to Fahrenheit: 80°C
        result = convert_temperature(80.0, from_celsius=True)
        assert result == 176.0
        
        # Fahrenheit to Celsius: 200°F
        result = convert_temperature(200.0, from_celsius=False)
        assert abs(result - 93.33) < 0.1


class TestDrillingScenarios:
    """Test realistic drilling scenarios with typical industry values."""
    
    def test_offshore_drilling_scenario(self):
        """Test a realistic offshore drilling scenario with mixed units."""
        # Water depth: 1500 meters = 4921 feet
        water_depth_ft = UnitConverter.convert_value(1500.0, WITSUnits.METERS, WITSUnits.FEET)
        assert abs(water_depth_ft - 4921.26) < 0.1
        
        # Drilling rate: 45 M/HR = 147.6 F/HR
        rop_fps = UnitConverter.convert_value(45.0, WITSUnits.MHR, WITSUnits.FHR)
        assert abs(rop_fps - 147.64) < 0.1
        
        # Standpipe pressure: 2500 PSI = 17237 KPA
        pressure_kpa = UnitConverter.convert_value(2500.0, WITSUnits.PSI, WITSUnits.KPA)
        assert abs(pressure_kpa - 17236.9) < 1.0
        
        # Mud flow rate: 900 GPM = 3407 LPM
        flow_lpm = UnitConverter.convert_value(900.0, WITSUnits.GPM, WITSUnits.LPM)
        assert abs(flow_lpm - 3406.86) < 1.0
        
        # Mud density: 12.5 PPG = 1497 KG/M3
        density_kgm3 = UnitConverter.convert_value(12.5, WITSUnits.PPG, WITSUnits.KGM3)
        assert abs(density_kgm3 - 1497.01) < 1.0
    
    def test_onshore_drilling_scenario(self):
        """Test a realistic onshore drilling scenario."""
        # Total depth: 8000 feet = 2438.4 meters
        td_meters = UnitConverter.convert_value(8000.0, WITSUnits.FEET, WITSUnits.METERS)
        assert abs(td_meters - 2438.4) < 0.1
        
        # Drilling rate: 120 F/HR = 36.58 M/HR
        rop_metric = UnitConverter.convert_value(120.0, WITSUnits.FHR, WITSUnits.MHR)
        assert abs(rop_metric - 36.576) < 0.1
        
        # Bottom hole temperature: 180°F = 82.22°C
        bht_celsius = UnitConverter.convert_value(180.0, WITSUnits.DEGF, WITSUnits.DEGC)
        assert abs(bht_celsius - 82.22) < 0.1
        
        # Weight on bit: 30 KLB = 133.45 KDN
        wob_kdn = UnitConverter.convert_value(30.0, WITSUnits.KLB, WITSUnits.KDN)
        assert abs(wob_kdn - 133.45) < 0.1
        
        # Torque: 25 KFLB = 33.9 KNM
        torque_knm = UnitConverter.convert_value(25.0, WITSUnits.KFLB, WITSUnits.KNM)
        assert abs(torque_knm - 33.9) < 0.1
    
    def test_high_pressure_scenario(self):
        """Test high pressure drilling scenario."""
        # High pressure well: 15000 PSI = 103421 KPA
        hp_kpa = UnitConverter.convert_value(15000.0, WITSUnits.PSI, WITSUnits.KPA)
        assert abs(hp_kpa - 103421.4) < 10.0
        
        # Heavy mud: 18 PPG = 2157 KG/M3
        heavy_mud = UnitConverter.convert_value(18.0, WITSUnits.PPG, WITSUnits.KGM3)
        assert abs(heavy_mud - 2157.02) < 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
