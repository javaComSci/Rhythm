import React from 'react';
import { AppRegistry } from 'react-native';
import { createStackNavigator, createAppContainer } from "react-navigation";
import {
  reduxifyNavigator,
  createReactNavigationReduxMiddleware,
  createNavigationReducer,
} from 'react-navigation-redux-helpers';
import HomeScreen from './HomeScreen';
import ProfileScreen from './ProfileScreen';
import CompositionScreen from './CompositionScreen';
import { Provider, connect } from 'react-redux';
import { addComposition } from './Actions/composition';
import {
  createStore,
  applyMiddleware,
  combineReducers,
} from 'redux';


state = {
  userEmail: '',
  userCompositions: []
}
/*
Create the stack navigator
*/
const AppNavigator = createStackNavigator(
  {
    Home: HomeScreen,
    Profile: ProfileScreen,
    Compositions: CompositionScreen
  },
  {
    initialRouteName: "Home"
  }
);

const navReducer = createNavigationReducer(AppNavigator);
const appReducer = combineReducers({
  nav: navReducer
})

const middleware = createReactNavigationReduxMiddleware(
  "root",
  state => state.nav,
)

const App = reduxifyNavigator(AppNavigator, "root");

const mapStateToProps = (state) => ({
  state: state.nav
});

const AppWithNavigationState = connect(mapStateToProps)(App);

const store = createStore(
  appReducer,
  applyMiddleware(middleware),
);

class Root extends React.Component {
  render() {
    return (
      <Provider store={store}>
        <AppWithNavigationState />
      </Provider>
    )
  }
}

export default Root
// const MainApplication = createAppContainer(AppNavigator)

// class AppNavigation extends Component {
//   constructor(props) {
//     super(props);
//   }

//   render() {
//     return <MainApplication screenProps={this.props} />
//   }
// }

// /*
// Create the app container
// */

// export default class App extends React.Component {
//   render() {
//     return (
//       <Provider store={store}>
//         <AppNavigator />
//       </Provider>
//     )
//   }
// }
