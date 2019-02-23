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
        case 'ADD_EMAIL':
            return {
                ...state, isRegistered: action.email
            };
        case 'ADD_USERID':
            console.log('user id route nav')
            return {
                ...state, id: action.id
            };
        default:
            nextState = RootNavigator.router.getStateForAction(action, state);
            break;
    }

    return nextState || state;
}

const initalRegisterState = { isRegistered: false, id: "26342" };

function auth(state = initalRegisterState, action) {
    switch (action.type) {
        case 'ADD_EMAIL':
            return { ...state, isRegistered: action.email }; //duplicate
        case 'ADD_USERID':
            console.log('user id route auth')
            return { ...state, id: action.id }
        default:
            return state;
    }
}

const AppReducer = combineReducers({
    nav,
    auth
});

export default AppReducer;
