import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { createStackNavigator } from 'react-navigation';
import {
  reduxifyNavigator,
  createReactNavigationReduxMiddleware,
} from 'react-navigation-redux-helpers';

import HomeScreen from '../components/HomeScreen';
import ProfileScreen from '../components/ProfileScreen';
import CompositionScreen from '../components/CompositionScreen';
import RegisterScreen from '../components/RegisterScreen';
import ViewCompScreen from '../components/ViewCompScreen';

const middleware = createReactNavigationReduxMiddleware(
  'root',
  state => state.nav
)

const RootNavigator = createStackNavigator({
  Home: { screen: HomeScreen },
  Profile: { screen: ProfileScreen },
  Composition: { screen: CompositionScreen },
  Register: { screen: RegisterScreen },
  ViewCompScreen: { screen: ViewCompScreen },
});

const AppWithNavigationState = reduxifyNavigator(RootNavigator, 'root');

const mapStateToProps = state => ({
  state: state.nav,
});

const AppNavigator = connect(mapStateToProps)(AppWithNavigationState);

export { RootNavigator, AppNavigator, middleware };
