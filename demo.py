from src.posture import extract_features, classify_posture

points = {"shoulder":(0,0),"hip":(0,2),"knee":(1,4),"ankle":(2,5)}
features = extract_features(points)
print("Features:", features)
print("Posture:", classify_posture(features))
