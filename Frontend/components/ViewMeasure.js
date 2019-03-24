/**
 * importing all the things I need to make this monster.
 * This includes but not limited to, React, react-native, react-redux,
 * react-native-easy-Grid, react-native-vector-icons/AntDesign
 * react-native-pinch-zoom-view, expo, and most importantly SVG.
 */

import React from 'react';
  import { ListItem, PanResponder, Dimensions,TextInput, Alert, FlatList, TouchableOpacity, ScrollView, StyleSheet, View, KeyboardAvoidingView, Image, ImageBackground } from 'react-native';
  // import { Header } from 'react-navigation';
  import { connect } from 'react-redux';
  import { Button, Header } from 'react-native-elements';
  import { Col, Row, Grid } from "react-native-easy-grid";
  import Icon from 'react-native-vector-icons/AntDesign'
  import PinchZoomView from 'react-native-pinch-zoom-view';


  import { Svg } from 'expo';
  const { Circle, Rect, Path, Line, Text, G, Defs, Use } = Svg;

const SCREEN_WIDTH = Dimensions.get('window').width
const SCREEN_HEIGHT = Dimensions.get('window').height

var NoteSVG = require('./jsons/NotesData.json');
var MiscJson = require('./jsons/EditMisc.json');

let MeasureNoteList = [];


class ViewMeasure extends React.Component {

  constructor(props) {
      super(props);
      console.log("constructor: ");
      MeasureNoteList = this.props.navigation.getParam('arr');
      this.state = {
      };
  }

  static navigationOptions = {
      title: 'Welcome', header: null
  };

  componentDidMount() {}

  componentWillMount() {}

  VerticalSection(x, y){
    return (
      <Svg height="100%" width="100%">
        <Line
            x1={[x].join(' ')}
            y1={[y].join(' ')}
            x2={[x].join(' ')}
            y2={[y+(4*(SCREEN_HEIGHT/36.5))].join(' ')}
            stroke="black"
            strokeWidth="2"
        />
      </Svg>
    )
  }

  lineSection(){
    // console.log(totalBeats);
    let Measures = [];
    let spaceBetween = SCREEN_HEIGHT/82;
    let mesureLength = SCREEN_WIDTH/10;
    let start = SCREEN_HEIGHT/8;
    let betweenNotes = SCREEN_WIDTH/11;
    return (
      <Svg height="100%" width="100%">
        <Path x={[mesureLength].join(' ')} y={[SCREEN_HEIGHT/3].join(' ')} transform={['scale(', 1.5, .9, ')'].join(' ')}  style="fill:green"
        d={[MiscJson[0].data].join(' ')}/>
        {this.VerticalSection(SCREEN_WIDTH/10,SCREEN_HEIGHT/3)}
        {this.VerticalSection(SCREEN_WIDTH/1.11,SCREEN_HEIGHT/3)}
      </Svg>
    )
  }

  NotesEditRender(){
    let FirstNote = SCREEN_WIDTH/9;
    let start = SCREEN_HEIGHT/8;
    let betweenNotes = (SCREEN_WIDTH/(MeasureNoteList.length+.2));
    let Notes = [];
    for (var i = 0; i < MeasureNoteList.length; i++) {
    // for (let i = 0; i < 1; i++) {
      let x = FirstNote + (i * betweenNotes + (NoteSVG[MeasureNoteList[i].props.note].adjustX * 2));
      // let x = (i * betweenNotes + (NoteSVG[MeasureNoteList[i].props.note].adjustX * 2));
      // MeasureNoteList[i].props
      /* rendering the path of the note num */
      Notes.push(
        <G stroke="black" stroke-width="0" fill="black">
          <Path x={[x].join(' ')} y={([280].join(' '))} transform={['scale(', NoteSVG[MeasureNoteList[i].props.note].scale1 * 2, NoteSVG[MeasureNoteList[i].props.note].scale2 * 2, ')'].join(' ')} d={[NoteSVG[MeasureNoteList[i].props.note].data].join(' ')}/>
        </G>
      )
    }
    return Notes;
  }

  render(){
    console.log("viewMeasure Render\n");
    return (
      <View style={styles.container}>
        <Header
          statusBarProps={{ barStyle: 'light-content' }}
          barStyle="light-content" // or directly
          leftComponent={
            <Button
              onPress={() => this.props.navigation.navigate('EditMusicScreen')}
              icon={
                <Icon
                  name="left"
                  size={15}
                  color="white"
                />
              }
              type="clear"
            />
          }
          centerComponent={{ text: 'Rhythm', style: { color: '#fff' } }}
          containerStyle={{
            backgroundColor: 'green',
            justifyContent: 'space-around',
          }}
        />
        <Svg height="100%"  width="100%">
          {this.lineSection()}
          {this.lineSection()}
          {this.NotesEditRender()}
        </Svg>
      </View>
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

  export default connect(mapStateToProps, mapDispatchToProps)(ViewMeasure);


// import React,{ Component } from 'react';
// import { connect } from 'react-redux';
// import {
//     StyleSheet,
//     View,
//     Text,
//     PanResponder,
//     Animated,
//     Easing,
//     Dimensions
// } from 'react-native';
//
// class ViewMeasure extends Component{
//     constructor(props){
//         super(props);
//
//         this.state = {
//             showDraggable   : true,
//             dropZoneValues  : null,
//             pan             : new Animated.ValueXY()
//         };
//
//         this.panResponder = PanResponder.create({
//             onStartShouldSetPanResponder    : () => true,
//             onPanResponderMove              : Animated.event([null,{
//                 dx  : this.state.pan.x,
//                 dy  : this.state.pan.y
//             }]),
//             onPanResponderRelease           : (e, gesture) => {
//                 if(this.isDropZone(gesture)){
//                     this.setState({
//                         showDraggable : false
//                     });
//                 }else{
//                     Animated.spring(
//                         this.state.pan,
//                         {toValue:{x:0,y:0}}
//                     ).start();
//                 }
//             }
//         });
//     }
//
//
//     isDropZone(gesture){
//         var dz = this.state.dropZoneValues;
//         return gesture.moveY > dz.y && gesture.moveY < dz.y + dz.height;
//     }
//
//     setDropZoneValues(event){
//         this.setState({
//             dropZoneValues : event.nativeEvent.layout
//         });
//     }
//
//     render(){
//         return (
//             <View style={styles.mainContainer}>
//                 <View
//                     onLayout={this.setDropZoneValues.bind(this)}
//                     style={styles.dropZone}>
//                     <Text style={styles.text}>Drop me here!</Text>
//                 </View>
//
//                 {this.renderDraggable()}
//             </View>
//         );
//     }
//
//     renderDraggable(){
//         if(this.state.showDraggable){
//             return (
//                 <View style={styles.draggableContainer}>
//                     <Animated.View
//                         {...this.panResponder.panHandlers}
//                         style={[this.state.pan.getLayout(), styles.circle]}>
//                         <Text style={styles.text}>Drag me!</Text>
//                     </Animated.View>
//                 </View>
//             );
//         }
//     }
// }
//
// function mapStateToProps(state) {}
//
// function mapDispatchToProps(dispatch) {}
//
//
// let CIRCLE_RADIUS = 36;
// let Window = Dimensions.get('window');
// let styles = StyleSheet.create({
//     mainContainer: {
//         flex    : 1
//     },
//     dropZone    : {
//         height  : 100,
//         backgroundColor:'#2c3e50'
//     },
//     text        : {
//         marginTop   : 25,
//         marginLeft  : 5,
//         marginRight : 5,
//         textAlign   : 'center',
//         color       : '#fff'
//     },
//     draggableContainer: {
//         position    : 'absolute',
//         top         : Window.height/2 - CIRCLE_RADIUS,
//         left        : Window.width/2 - CIRCLE_RADIUS,
//     },
//     circle      : {
//         backgroundColor     : '#1abc9c',
//         width               : CIRCLE_RADIUS*2,
//         height              : CIRCLE_RADIUS*2,
//         borderRadius        : CIRCLE_RADIUS
//     }
// });
//
// export default connect(mapStateToProps, mapDispatchToProps)(ViewMeasure);
