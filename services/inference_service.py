from deploy import inference
from configs import config

def predict_service(model,device,sequence):

    # Kiểm tra model đã được load chưa
    if model is None or device is None:

        raise RuntimeError(
            "Model chưa được load. "
            "Hãy gọi load_model_service() trước."
        )


    # Gọi deploy predict
    label, confidence = inference.predict(
        sequence=sequence,
        model=model,
        device=device,
        classes=config.categories
    )


    return {
        "label": label,
        "confidence": confidence
    }