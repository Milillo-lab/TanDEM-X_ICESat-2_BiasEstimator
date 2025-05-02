
# TanDEM-X Bias Estimation based on ICESat-2

**AI-Driven TanDEM-X Penetration Bias Estimation in Antarctica Using ICESat-2 and ECMWF Data**

---
<div align="center">

**Ankita Vashishtha<sup>*,1</sup>**, **Pietro Milillo<sup>1,2,3</sup>**, **Alexandre Becker Campos<sup>3,5</sup>**, **Jose Luis Bueso Bello<sup>3</sup>**, **Paola Rizzoli<sup>3</sup>**, **Johan Nilsson<sup>4</sup>**


<sup>1</sup> Department of Civil and Environmental Engineering, University of Houston, Houston, TX, USA  
<sup>2</sup> Department of Earth and Atmospheric Science, University of Houston, Houston, TX, USA  
<sup>3</sup> German Aerospace Centre (DLR), Microwaves and Radar Institute, Munich, Germany  
<sup>4</sup> Jet Propulsion Laboratory, California Institute of Technology, Pasadena, CA, USA  
<sup>5</sup> FAU Erlangen- Nürnberg, Institute of Geography, Erlangen, Germany

<sup>*</sup>Corresponding author: [Ankita Vashishtha](mailto:avashish@CougarNet.UH.EDU)

[![Paper](https://img.shields.io/badge/Published%20In-The%20Cryosphere-blue)](https://arxiv.org/abs/)
[![Zenodo](https://img.shields.io/badge/Zenodo-link-green)](https://zenodo.org/records/15321465?preview=1&token=eyJhbGciOiJIUzUxMiIsImlhdCI6MTc0NjE2NTc3MCwiZXhwIjoxNzY5ODE3NTk5fQ.eyJpZCI6IjA5ODU2ZGEzLWNhNGUtNDI0Ny04OTVjLTM2YWNjMWQyYzdkYSIsImRhdGEiOnt9LCJyYW5kb20iOiJiZjVkMDNkZTJiOWQxOGZkNzczZGY2MzcxNWQ3MmY2YyJ9.wNoHk4a4BTu-dg0_K_hvQ_01Rc5dKtJ52JipmrxpCXUquUPCHoQiz3r_QU7WW7Lsx5MhYtvk3-_QkaYEIBQ7NA)
[![MIT License](https://img.shields.io/badge/License-MIT-929292.svg)](https://github.com/Milillo-lab/TanDEM-X_ICESat-2_BiasEstimator/blob/main/LICENSE.txt)

</div>

## How To CIte


## Overview

This project presents a machine learning and deep learning approach to estimate and correct penetration biases in TanDEM-X (TDX) elevation measurements over Grounding Lines in Antarctica using ICESat-2 laser altimetry and ECMWF ERA5 atmospheric data. Penetration bias correction enhances the accuracy of radar-derived digital elevation models (DEMs), critical for reliable glaciological assessments and monitoring polar ice mass balance.

The repository includes:
- Datasets extracted from TanDEM-X, ICESat-2, and ECMWF (Zenodo).
- Jupyter notebooks for data preprocessing, model training, evaluation, and prediction.
- Pre-trained model weights.
- Scripts for automated data preparation.

Findings from this study contribute to NASA's [Surface Topography and Vegetation (STV) Decadal Survey study](https://science.nasa.gov/earth-science/decadal-surveys/decadal-stv/), proposing a novel approach to mitigate radar elevation bias in polar regions.

## Funding: 
This work was conducted at the University of Houston, TX under a contract with the Cryosphere Program of NASA, and the NASA Decadal Survey Incubation program.	

## Study Area Overview
Here is the overview map of the analyzed region:
![Overview Map of Study Area](figures/Overall_Map.jpeg)

---

## Repository Structure

```plaintext
TanDEM-X_ICESat-2_BiasEstimator/
├── README.md
├── LICENSE
├── CITATION.cff
├── .gitignore
├── data/
│   └── Input_fil_data.csv
├── notebooks/
│   ├── 01_Data_Preprocessing.ipynb
│   ├── 02_Model_Training.ipynb
│   ├── 03_Model_Evaluation.ipynb
│   └── 04_Predict_PenetrationBias.ipynb
├── models/ [on Zenodo]
│   ├── trained_model_DNN.h5
│   └── trained_model_RF.pkl
├── scripts/
│   ├── download_ecmwf_features.py
│   └── prepare_dataset.py
├── requirements.txt
└── figures/

```

---

## Installation

Clone this repository:

```bash
git clone https://github.com/Milillo-lab/TanDEM-X_ICESat-2_BiasEstimator.git
cd TanDEM-X_ICESat-2_BiasEstimator
```

Create a virtual environment (optional but recommended):

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## How to Use

### 1. Data Preparation
- If needed, run `scripts/prepare_dataset.py` to generate the input CSV by extracting features from raster datasets.

### 2. Training
- Open and run `notebooks/02_Model_Training.ipynb` to train machine learning and deep learning models.
- Pre-trained models are already available on [Zenodo](https://zenodo.org/records/15321465?preview=1&token=eyJhbGciOiJIUzUxMiIsImlhdCI6MTc0NjE2NTc3MCwiZXhwIjoxNzY5ODE3NTk5fQ.eyJpZCI6IjA5ODU2ZGEzLWNhNGUtNDI0Ny04OTVjLTM2YWNjMWQyYzdkYSIsImRhdGEiOnt9LCJyYW5kb20iOiJiZjVkMDNkZTJiOWQxOGZkNzczZGY2MzcxNWQ3MmY2YyJ9.wNoHk4a4BTu-dg0_K_hvQ_01Rc5dKtJ52JipmrxpCXUquUPCHoQiz3r_QU7WW7Lsx5MhYtvk3-_QkaYEIBQ7NA).
  
### 3. Evaluation
- Run `notebooks/03_Model_Evaluation.ipynb` to evaluate model performance.

### 4. Bias Prediction
- Use `notebooks/04_Predict_PenetrationBias.ipynb` to predict penetration bias on new TanDEM-X datasets.

---

## Dataset

The dataset consists of about 300,000 matched points with:
- ICESat-2 surface elevation.
- TanDEM-X DEM height and radar features (coherence, amplitude, slope, etc.).
- Atmospheric features from ECMWF ERA5 (temperature, snowfall, wind speed/direction, surface pressure).

**Note:** Due to size limitations, only a sample dataset is hosted here. The full dataset is available on [Zenodo](https://zenodo.org/records/15321465?preview=1&token=eyJhbGciOiJIUzUxMiIsImlhdCI6MTc0NjE2NTc3MCwiZXhwIjoxNzY5ODE3NTk5fQ.eyJpZCI6IjA5ODU2ZGEzLWNhNGUtNDI0Ny04OTVjLTM2YWNjMWQyYzdkYSIsImRhdGEiOnt9LCJyYW5kb20iOiJiZjVkMDNkZTJiOWQxOGZkNzczZGY2MzcxNWQ3MmY2YyJ9.wNoHk4a4BTu-dg0_K_hvQ_01Rc5dKtJ52JipmrxpCXUquUPCHoQiz3r_QU7WW7Lsx5MhYtvk3-_QkaYEIBQ7NA).

---

## Results Summary

- Achieved mean penetration bias correction of ~1 cm.
- Root Mean Square Error of TDX DEM (RMSE) ~1 m.
- Maximum errors on the order of 10 m.
- DNN and Random Forest models outperform other algorithms.
- Environmental features (temperature, wind speed) improved bias prediction by 10-20%.
- Valid for biases observed within -10 and +10 meters
---

## License

This project is licensed under the [MIT License](./LICENSE).

---

## Citation

If you use this code or dataset, please cite our work:

```bibtex
@misc{milillo2025,
  author = {Milillo, Pietro and Vashishtha, Ankita and Campos, Alexandre Becker and Bueso Bello, Jose Luis and Rizzoli, Paola and Nilsson, Johan},
  title = {AI-Driven TanDEM-X Penetration Bias Estimation in Antarctica Using ICESat-2 and ECMWF Data},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished = {\url{https://github.com/Milillo-lab/TanDEM-X_ICESat-2_BiasEstimator}}
}
```

---

## Acknowledgements

- NASA Cryosphere Program
- NASA Decadal Survey Incubation Program
- German Aerospace Center (DLR)
- Copernicus Climate Change Service (C3S) for ECMWF ERA5 data
- NSIDC and NASA ICESat-2 Mission

We gratefully acknowledge the support of our collaborators and funding agencies.

---

## Contact

For questions or collaboration inquiries:
- Pietro Milillo: [pmilillo@cougarnet.uh.edu](mailto:pmilillo@cougarnet.uh.edu)
- GitHub Issues: [Open an Issue](https://github.com/Milillo-lab/TanDEM-X_ICESat-2_BiasEstimator/issues)

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

