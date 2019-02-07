import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { createStackNavigator, createAppContainer } from "react-navigation";
import HomeScreen from './HomeScreen';
import ProfileScreen from './ProfileScreen';
import CompositionScreen from './CompositionScreen';

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

/*
Create the app container
*/
export default createAppContainer(AppNavigator); // 
