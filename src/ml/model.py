import io

import torch
import torchvision.models as models
from PIL import Image
from torch import nn
from torchvision import transforms


class Model:
    def __init__(self):
        self.classes = ['basil_downy_mildew',
                        'basil_healthy',
                        'basil_wilted',
                        'lettuce_bacterial_spot',
                        'lettuce_downy_mildew',
                        'lettuce_healthy',
                        'lettuce_powdery_mildew',
                        'lettuce_septoria',
                        'strawberry_grey_mold',
                        'strawberry_healthy',
                        'strawberry_leaf_spot',
                        'strawberry_leaves_ scorch',
                        'strawberry_powdery_mildew',
                        'tomato_bacterial_spot',
                        'tomato_blight',
                        'tomato_fusarium_wilt',
                        'tomato_healthy',
                        'tomato_leaf_mold',
                        'tomato_mosaic_virus',
                        'tomato_septoria_leaf_spot',
                        'tomato_spider_mites',
                        'tomato_yellow_curl_virus']
        self.transforms = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize((0.4543, 0.4977, 0.3682), (0.2110, 0.1990, 0.2325))
        ])
        self.device = self._get_device()
        self.model = self._get_model()
        self.model.load_state_dict(torch.load('/Users/yuliakarpova/Documents/диплом/PlantsProject/src/ml/resnet50_acc08', map_location=self.device))

    def eval_model(self, content: bytes):
        transformed_image = self._preprocess_image(content)
        self.model.eval()

        with torch.no_grad():
            input_tensor = torch.tensor(transformed_image).unsqueeze(0)
            output = self.model(input_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1)
            _, predicted_classes = torch.max(output, dim=1)

            predicted_class = predicted_classes[0].item()
            probability = probabilities[0][predicted_class].item()

            plant_with_disease = self.classes[predicted_class]
            result = plant_with_disease.split('_')
            plant_type = result[0]
            plant_disease = ' '.join(result[1:])

            return plant_type, plant_disease, probability

    def _preprocess_image(self, content: bytes):
        img = Image.open(io.BytesIO(content))
        return self.transforms(img)

    def _get_model(self, print_model=False):

        resnet_model = models.resnet50(pretrained=True)

        num_features = resnet_model.fc.in_features
        resnet_model.fc = nn.Sequential(nn.Linear(num_features, len(self.classes)))

        if print_model:
            print(resnet_model)

        return resnet_model

    def _get_device(self):
        if torch.cuda.is_available():
            device = torch.device('cuda:0')
        else:
            device = torch.device('cpu')

        return device
