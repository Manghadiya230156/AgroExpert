"""Educational descriptions for PlantVillage disease labels.

Advice is general and should not replace local agricultural extension guidance.
"""
import re

KNOWN = {
    "Apple___Apple_scab": (
        "Apple scab is a fungal disease that can cause olive-green to dark, scabby lesions on leaves and fruit.",
        ["Remove fallen infected leaves and fruit where practical.", "Improve airflow by pruning appropriately and avoid prolonged leaf wetness.", "Choose resistant varieties where available and ask a local extension officer about locally approved fungicides."],
    ),
    "Apple___Black_rot": (
        "Black rot is a fungal disease that may cause leaf spots and dark, sunken fruit lesions.",
        ["Remove mummified fruit and infected dead wood.", "Prune to improve airflow and avoid injuring branches.", "Use only locally registered treatments recommended for the crop and region."],
    ),
    "Corn_(maize)___Common_rust_": (
        "Common rust usually produces small, reddish-brown raised pustules on maize leaves.",
        ["Scout leaves regularly, especially in humid weather.", "Use resistant hybrids when available and manage volunteer maize plants.", "Seek local advice before applying a fungicide; timing matters."],
    ),
    "Potato___Early_blight": (
        "Early blight commonly causes brown leaf spots with concentric rings, often on older leaves first.",
        ["Rotate away from potatoes and tomatoes where feasible.", "Remove infected crop debris and avoid water stress.", "Use clean seed tubers and locally recommended disease management."],
    ),
    "Potato___Late_blight": (
        "Late blight can spread rapidly in cool, wet conditions and may cause water-soaked lesions with pale growth beneath leaves.",
        ["Act quickly and contact a local agricultural extension service if suspected.", "Avoid moving infected plant material and do not compost diseased material unless local guidance permits.", "Use resistant varieties and only locally approved protection measures."],
    ),
    "Tomato___Bacterial_spot": (
        "Bacterial spot can cause small dark, sometimes water-soaked spots on tomato leaves and fruit.",
        ["Avoid handling plants while wet and reduce overhead irrigation.", "Use clean seed/transplants and sanitize tools.", "Remove heavily affected material carefully and follow local extension guidance."],
    ),
    "Tomato___Early_blight": (
        "Early blight often produces brown spots with target-like rings, usually starting on older tomato leaves.",
        ["Remove affected lower leaves and crop debris.", "Mulch to reduce soil splash, rotate crops, and water at the soil level.", "Maintain plant spacing and follow locally approved disease management advice."],
    ),
    "Tomato___Late_blight": (
        "Late blight is a potentially fast-moving disease that can cause irregular dark lesions on leaves and stems.",
        ["Seek local agricultural advice promptly if suspected.", "Avoid prolonged leaf wetness and remove infected plants as advised locally.", "Do not rely on this image prediction alone to choose a chemical treatment."],
    ),
    "Tomato___Leaf_Mold": (
        "Tomato leaf mold often causes pale yellow patches above leaves and olive-green to brown mold beneath them.",
        ["Improve greenhouse or canopy ventilation.", "Avoid wetting foliage and reduce excess humidity where possible.", "Remove infected debris and seek locally suitable disease management advice."],
    ),
    "Tomato___Septoria_leaf_spot": (
        "Septoria leaf spot typically causes many small circular spots with pale centers and dark margins.",
        ["Remove infected lower leaves and crop debris.", "Use mulch to limit soil splash and rotate crops.", "Water at the soil level and improve airflow around plants."],
    ),
    "Tomato___Spider_mites Two-spotted_spider_mite": (
        "Spider mites are pests rather than a fungal disease; feeding may cause fine stippling, bronzing, and webbing.",
        ["Inspect leaf undersides with a hand lens.", "Reduce plant stress and conserve beneficial predatory insects.", "Confirm the pest before selecting a locally approved control method."],
    ),
    "Tomato___Target_Spot": (
        "Target spot can cause brown lesions with concentric rings on tomato leaves and sometimes fruit.",
        ["Remove crop debris and avoid extended leaf wetness.", "Provide adequate spacing and airflow.", "Confirm the diagnosis locally because several leaf diseases look similar."],
    ),
    "Tomato___Yellow_Leaf_Curl_Virus": (
        "Tomato yellow leaf curl virus can cause upward leaf curling, yellowing, and stunted growth; whiteflies can spread it.",
        ["Inspect for whiteflies and manage them using integrated pest management.", "Remove severely affected plants according to local guidance and control nearby weed hosts.", "Use resistant varieties and healthy seedlings where available."],
    ),
    "Tomato___Mosaic_virus": (
        "Tomato mosaic virus may cause mottled light/dark leaves, distortion, and reduced growth.",
        ["Wash hands and sanitize tools between plants.", "Use certified healthy seed and avoid tobacco contamination when handling plants.", "Remove infected plants as advised locally; there is no curative spray for a virus."],
    ),
}


def _humanize(label):
    crop, _, condition = label.partition("___")
    crop = crop.replace("_", " ").replace("(", "").replace(")", "").strip()
    condition = condition.replace("_", " ").strip()
    condition = re.sub(r"\s+", " ", condition)
    if condition.lower() == "healthy":
        return crop, "Healthy", True
    return crop, condition or "Unclassified condition", False


def get_disease_guidance(label):
    if label in KNOWN:
        explanation, prevention = KNOWN[label]
        crop, condition, healthy = _humanize(label)
    else:
        crop, condition, healthy = _humanize(label)
        if healthy:
            explanation = f"The model classifies this {crop} leaf as healthy based on the visual patterns learned during training. This does not rule out early disease or problems not represented in the training data."
            prevention = ["Continue regular scouting, including the underside of leaves.", "Use clean planting material, suitable spacing, and balanced irrigation.", "Recheck the plant if symptoms develop; seek local expert advice when uncertain."]
        else:
            explanation = f"The model's closest learned category is {condition} on {crop}. Leaf-image models can confuse diseases with similar visual symptoms, so treat this as a screening result rather than a confirmed diagnosis."
            prevention = ["Inspect several leaves and the whole plant for matching symptoms.", "Remove heavily affected plant material only when recommended for this crop and disease.", "Improve airflow, avoid unnecessary leaf wetness, and clean tools between plants.", "Consult a local agricultural extension officer before applying pesticides or fungicides."]
    return {"crop": crop, "condition": condition, "healthy": healthy, "explanation": explanation, "prevention": prevention}
