import { combineReducers } from 'redux';
import { NavigationActions } from 'react-navigation';
import { RootNavigator } from '../navigators/AppNavigation';

const homeAction = RootNavigator.router.getActionForPathAndParams('Home');
const initialNavState = RootNavigator.router.getStateForAction(
    homeAction,
    initialNavState
);

function nav(state = initialNavState, action) {
    let nextState;
    console.log(action); //debug
    switch (action.type) {
        /*
        case 'NameOfAction':
            nextState = RootNavigator.router.getStateForAction(
                *do things*,
                state
            );
            break;
        */
        default:
            nextState = RootNavigator.router.getStateForAction(action, state);
            break;
    }

    return nextState || state;
}

const AppReducer = combineReducers({
    nav,
});

export default AppReducer;