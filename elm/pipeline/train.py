import copy
from functools import partial
import logging
import numbers

from elm.config import import_callable
from elm.model_selection.util import get_args_kwargs_defaults, ModelArgs
from elm.pipeline.ensemble import ensemble
from elm.pipeline.evolve_train import evolve_train, evolve_transform
from elm.pipeline.serialize import load_models_from_tag
from elm.pipeline.util import make_model_args_from_config

logger = logging.getLogger(__name__)


def _train_or_transform_step(train_or_transform,
                             config,
                             step,
                             client,
                             **kwargs):
    '''Evaluate a "train" step in a config's "pipeline"

    Params:
        train_or_transform: string - "train" or "transform"
        config:  config from elm.config.ConfigParser
        step:    current step dictionary in config's pipeline,
        client: None or a threaded/process/distributed Executor
        kwargs:
    Returns:
        models: the fitted models in the ensemble
    '''
    from elm.pipeline.transform import get_new_or_saved_transform_model
    (_, sample_pipeline, data_source, transform_model, samples_per_batch) = kwargs['sample_pipeline_info']
    evo_params = kwargs.get('evo_params') or None
    model_args, ensemble_kwargs = make_model_args_from_config(config,
                                                              step,
                                                              train_or_transform,
                                                              sample_pipeline,
                                                              data_source)
    sample_pipeline_info = kwargs.get('sample_pipeline_info') or None
    if not sample_pipeline_info:
        raise ValueError('Expected sample_pipeline_info')
    transform_model = kwargs.get('transform_model') or None

    if transform_model is None:
        transform_model = get_new_or_saved_transform_model(config,
                                                           sample_pipeline,
                                                           data_source,
                                                           step)
    if evo_params is not None:
        args = (client,
                step,
                evo_params,
                kwargs.get('transform_model') or None,
                sample_pipeline_info,)
        if train_or_transform == 'train':
            return evolve_train(*args, **ensemble_kwargs)
        return evolve_transform(*args, **ensemble_kwargs)
    models = ensemble(client,
                      model_args,
                      transform_model,
                      sample_pipeline_info,
                      **ensemble_kwargs)
    return models


train_step = partial(_train_or_transform_step, 'train')

