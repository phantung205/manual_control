import torch


def predict(sequence,model, device,classes):
    # kiểm tra xem shap có đúng ko
    if sequence.shape != (30, 63):
        raise ValueError(
            f"Sequence phải có shape (30, 63), "
            f"nhưng nhận được {sequence.shape}"
        )

    # chuyện sang dạng tensor
    sequence = torch.tensor(sequence,dtype=torch.float32)

    # thêm chiều batch vào
    sequence = sequence.unsqueeze(0)

    # cho vào device
    sequence = sequence.to(device)

    # inference
    with torch.no_grad():
        outputs = model(sequence)

        # Softmax
        probabilities = torch.softmax(outputs,dim=1)


        # max probability
        confidence, predicted = torch.max(probabilities,dim=1)

        # Tensor → Python
    confidence = confidence.item()

    predicted = predicted.item()

    # index → class name
    label = classes[predicted]

    return label, confidence