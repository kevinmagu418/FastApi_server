# MODEL_REGISTRY with paths pointing to weights folder
MODEL_REGISTRY = {
    "apple": {
        "classes": [
            "Apple___Apple_scab",
            "Apple___Black_rot",
            "Apple___Cedar_apple_rust",
            "Apple___healthy"
        ],
        "display_classes": [
            "Apple scab",
            "Black rot",
            "Cedar apple rust",
            "Healthy"
        ],
        "model_path": "app/models/weights/apple.pth"
    },
    "bean": {
    "classes": ["Angular_Leaf_Spot", "Bean_Rust", "Healthy"],
    "display_classes": ["Angular Leaf Spot", "Bean Rust", "Healthy"],
    "model_path": "app/models/weights/beans.pth"
},
    "bellpepper": {
        "classes": [
            "Pepper,_bell___Bacterial_spot",
            "Pepper,_bell___healthy"
        ],
        "display_classes": ["Bacterial spot", "Healthy"],
        "model_path": "app/models/weights/bellpepper.pth"
    },
    "cassava": {
        "classes": [
            "Cassava___bacterial_blight",
            "Cassava___brown_streak_disease",
            "Cassava___green_mottle",
            "Cassava___healthy",
            "Cassava___mosaic_disease"
        ],
        "display_classes": [
            "Bacterial blight",
            "Brown streak disease",
            "Green mottle",
            "Healthy",
            "Mosaic disease"
        ],
        "model_path": "app/models/weights/cassava.pth"
    },
    "cherry": {
        "classes": [
            "Cherry_(including_sour)___Powdery_mildew",
            "Cherry_(including_sour)___healthy"
        ],
        "display_classes": ["Powdery mildew", "Healthy"],
        "model_path": "app/models/weights/cherry.pth"
    },
    "grape": {
        "classes": [
            "Grape___Black_rot",
            "Grape___Esca_(Black_Measles)",
            "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
            "Grape___healthy"
        ],
        "display_classes": [
            "Black rot",
            "Esca (Black Measles)",
            "Leaf blight (Isariopsis Leaf Spot)",
            "Healthy"
        ],
        "model_path": "app/models/weights/grape.pth"
    },
    "maize": {
        "classes": [
            "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
            "Corn_(maize)___Common_rust_",
            "Corn_(maize)___Northern_Leaf_Blight",
            "Corn_(maize)___healthy"
        ],
        "display_classes": [
            "Cercospora leaf spot Gray leaf spot",
            "Common rust",
            "Northern Leaf Blight",
            "Healthy"
        ],
        "model_path": "app/models/weights/maize.pth"
    },
    "peach": {
        "classes": ["Peach___Bacterial_spot", "Peach___healthy"],
        "display_classes": ["Bacterial spot", "Healthy"],
        "model_path": "app/models/weights/peach.pth"
    },
    "potato": {
        "classes": ["Potato___Early_blight", "Potato___Late_blight", "Potato___healthy"],
        "display_classes": ["Early blight", "Late blight", "Healthy"],
        "model_path": "app/models/weights/potato.pth"
    },
    "strawberry": {
        "classes": ["Strawberry___Leaf_scorch", "Strawberry___healthy"],
        "display_classes": ["Leaf scorch", "Healthy"],
        "model_path": "app/models/weights/strawberry.pth"
    },
    "tomato": {
        "classes": [
            "Tomato___Bacterial_spot",
            "Tomato___Early_blight",
            "Tomato___Late_blight",
            "Tomato___Leaf_Mold",
            "Tomato___Septoria_leaf_spot",
            "Tomato___Spider_mites Two-spotted_spider_mite",
            "Tomato___Target_Spot",
            "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
            "Tomato___Tomato_mosaic_virus",
            "Tomato___healthy"
        ],
        "display_classes": [
            "Bacterial spot",
            "Early blight",
            "Late blight",
            "Leaf Mold",
            "Septoria leaf spot",
            "Spider mites",
            "Target Spot",
            "Tomato Yellow Leaf Curl Virus",
            "Tomato mosaic virus",
            "Healthy"
        ],
        "model_path": "app/models/weights/tomato.pth"
    }
}
