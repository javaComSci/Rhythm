import React from 'react';
import { TextInput, FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View, KeyboardAvoidingView } from 'react-native';
import { Header } from 'react-navigation';
// import { Button } from 'react-native-elements';

var styles = require('../style');

class EditMusicScreen extends React.Component {
  constructor(props) {
      super(props);
      console.log("props,", props);
      console.log("store", this.props.store)
      this.state = {
          edit: false,
          emailText: "",
          email: "",
          name: "",
          nameText: "",
      };
  }
  render(){

  }
}
