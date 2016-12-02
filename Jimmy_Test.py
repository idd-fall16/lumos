# sound init
mpdport = "6600"
noise_tolerance = 2
prev_noise = 100
noise_m = 0.025
noise_b = 1.25
noise_max_converted = 100

# bulb init
is_manual = 1
color_tolerance = 500
bulb_tolerance = 1000

prev_color = 0
prev_brightness = 0
prev_kelvin = 0

bulb_m = 16.38375
bulb_b = 819.1875
bulb_max_converted = 65535

kelvin_m = 1.625
kelvin_b = 2418.75
kelvin_min_converted = 2500
kelvin_max_converted = 9000
kelvin_tolerance = 200 # no idea if this is correct

saturation = 65535

msg = "C48B48K48N48"
# msg = "C52B52K52N52"
# msg = "C4048B4048K4048N4048"
# msg = "C4052B4052K4052N4052"