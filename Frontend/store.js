import { createStore, combineReducers } from 'redux';
import placeReducer from './Reducers/compositionReducer';
import compositionReducer from './Reducers/compositionReducer';

const rootReducer = combineReducers({
    userCompositions: compositionReducer
});

const configureStore = () => {
    return createStore(rootReducer);
}

export default configureStore;