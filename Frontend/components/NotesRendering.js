import React from 'react';
import { ListItem, Dimensions,TextInput, Alert, FlatList, TouchableOpacity, ScrollView, StyleSheet, View, KeyboardAvoidingView, Image, ImageBackground } from 'react-native';
// import { Header } from 'react-navigation';
import { connect } from 'react-redux';
import { Button, Header } from 'react-native-elements';
import { Col, Row, Grid } from "react-native-easy-grid";
import Icon from 'react-native-vector-icons/AntDesign'
import PinchZoomView from 'react-native-pinch-zoom-view';

import { Svg } from 'expo';
const { Circle, Rect, Path, Line, Text, G, Defs, Use } = Svg;

class NotesRendering extends React.Component {

  constructor(props) {
    console.log("HERERERERE: " + this.props);
  }

  static navigationOptions = {
      title: 'Welcome', header: null
  };

  componentDidMount() {}

  render(){
    return (
      <Svg height={[screenSize].join(' ')}  width="100%">
        <Text>Fuck yeeeeee</Text>
      </Svg>
    )
  }
};

  function mapStateToProps(state) {}

  function mapDispatchToProps(dispatch) {}

  const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor:"white",
    },
    header: {
      flex: .13,
      backgroundColor: 'black',
    },
    button: {
      alignItems: 'center',
      top: '90%',
      right: '40%',
    },
    background: {
      resizeMode: 'cover',
    },
    list: {
      flex: 1,
      flexDirection: 'column',
      backgroundColor: 'pink',
    },
  });

  export default connect(mapStateToProps, mapDispatchToProps)(NotesRendering);
