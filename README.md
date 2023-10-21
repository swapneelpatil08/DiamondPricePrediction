# Machine Learning Project

Steps to run this program:
`conda create -p venv  python=3.9`
`conda activate venv/`
`python setup.py install`
`python src/pipelines/training_pipeline.py`
`python application.py`


OR

`conda deactivate && rm -rf build DimondPricePrediction.egg-info dist venv/ && conda create -p venv  python=3.9 -y && conda activate venv/ && python setup.py install && python application.py`
