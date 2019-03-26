/**
 * importing all the things I need to make this monster.
 * This includes but not limited to, React, react-native, react-redux,
 * react-native-easy-Grid, react-native-vector-icons/AntDesign
 * react-native-pinch-zoom-view, expo, and most importantly SVG.
 */

import React from 'react';
  import { ListItem, PanResponder, Dimensions,TextInput, Alert, FlatList, TouchableOpacity, ScrollView, StyleSheet, View, KeyboardAvoidingView, Image, ImageBackground, Button as Butt } from 'react-native';
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

var MeasureNoteList = [];
var NewMeasureNoteList = [];
var fullList = [];
var measureNum;


var keyvalue;

class NoteObjects extends React.Component {

  /**
   * This sets up the state and the functions to
   * change the state
   */
  constructor(props) {
    super(props);

    // console.log("Props:");
    // console.log(this.props);

    /* Sets up the state with note num, pitch, Location, and color */
    this.state = {
      note: this.props.note,
      color: this.props.color,
      x: this.props.x,
      y: this.props.y,
      pitch: this.props.pitch,
      editMode: 0,
    }
    // console.log(this.state);
    // console.log("\n\n");
    /* Binds this to pressed() so it can change state when called */
    this.pressed = this.pressed.bind(this);
    this.props.ChangeColor = this.pressed;
    this.ChangeNotePressed = this.ChangeNotePressed.bind(this);
    this.props.ChangeNote = this.ChangeNotePressed;
    this.editModePress = this.editModePress.bind(this);
    this.props.editMode = this.editModePress;
  }

  editModePress(mode) {
    console.log("PIZZA IS THE BEST" + mode);
  }
  /**
   * Changing the color of the note that was pressed
   * red -> black OR black -> red
   */
  pressed() {
    if (this.state.color == 'black') {
      this.setState({ color: "red" });
    } else if (this.state.color == 'red') {
      this.setState({ color: "black" });
    }
  }
  /**
   * Changes the note when called. Simple stuff!
   * @param n must be within the NotesData.json
   * @param n == -1 then delete the note
   */
  ChangeNotePressed(n) {
    console.log("ChangeNotePressed");
  }
  ChangeColor(n) {
    this.setState({ color: "red" });
  }
  // shouldComponentUpdate(nextProps) {
  //   console.log("WORKED\n");
  //   // console.log(nextProps);
  //   console.log(this.state);
  //   this.setState({});
  //   // console.log("ERGFAWFEAW\n");
  //   // console.log(nextProps);
  //     // if(JSON.stringify(this.props.user) !== JSON.stringify(nextProps.user)) // Check if it's a new user, you can also use some unique property, like the ID
  //     // {
  //     //        this.updateUser();
  //     // }
  // }
  /**
   * Renders the note with its path
   */
  render() {

    // console.log("Rendering Notes\n");
    // console.log(this.props);
    let mesureLength = SCREEN_WIDTH / 10;
    let start = SCREEN_HEIGHT / 8;
    let betweenNotes = SCREEN_WIDTH / 11;
    /* rendering the path of the note num */
    return (
      <G stroke="black" stroke-width="0" fill={this.state.color}>
        <Path x={[((this.state.x) * (betweenNotes)) + NoteSVG[this.state.note].adjustX].join(' ')} y={([((this.state.y) * (start)) + (this.props.pitch * SCREEN_HEIGHT / 164) + NoteSVG[this.state.note].adjustY].join(' '))} transform={['scale(', NoteSVG[this.state.note].scale1, NoteSVG[this.state.note].scale2, ')'].join(' ')} d={[NoteSVG[this.state.note].data].join(' ')} />
      </G>
    )
  }
};



class ViewMeasure extends React.Component {

  constructor(props) {
      super(props);
      fullList = this.props.navigation.getParam('full');
      MeasureNoteList = this.props.navigation.getParam('arr');
      measureNum = this.props.navigation.getParam('num');
      this.state = {
        verfColor: "green",
      };

  }

  static navigationOptions = {
      title: 'Welcome', header: null
  };

  componentDidMount() {}

  componentWillMount() {
    keyvalue = 0;
    NewMeasureNoteList = [];
  }

  VerticalSection(x, y){
    return (
      <Svg height="100%" width="100%" key={keyvalue++}>
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
      <Svg height="100%" width="100%" key={keyvalue}>
        <Path x={[mesureLength].join(' ')} y={[SCREEN_HEIGHT/3].join(' ')} transform={['scale(', 1.5, .9, ')'].join(' ')}  style="fill:green"
        d={[MiscJson[0].data].join(' ')}/>
        {this.VerticalSection(SCREEN_WIDTH/10,SCREEN_HEIGHT/3)}
        {this.VerticalSection(SCREEN_WIDTH/1.11,SCREEN_HEIGHT/3)}
      </Svg>
    )
  }

  NotesEditRender(){
    let s = 0;
    let betweenNotes = (SCREEN_WIDTH/(MeasureNoteList.length+2));
    if(MeasureNoteList[0].props.note == 0 || MeasureNoteList[0].props.note == 6){
      s++;
      betweenNotes = (SCREEN_WIDTH/(MeasureNoteList.length+1));
    }
    let FirstNote = SCREEN_WIDTH/9;
    let halfHeight = SCREEN_HEIGHT/3;
    // halfHeight += SCREEN_HEIGHT/80;
    let start = SCREEN_HEIGHT/8;

    let Notes = [];

    for (var i = s; i < MeasureNoteList.length; i++) {
    // for (let i = 0; i < 1; i++) {
      // console.log("PIZZAMNA: " + (betweenNotes + (NoteSVG[MeasureNoteList[i].props.note].adjustX * 2)));
      let x = FirstNote + ((i-s) * betweenNotes + (NoteSVG[MeasureNoteList[i].props.note].adjustX * 2));
      let y = halfHeight + (NoteSVG[MeasureNoteList[i].props.note].adjustY * 2) + (MeasureNoteList[i].props.pitch * SCREEN_HEIGHT/75);
      // let x = (i * betweenNotes + (NoteSVG[MeasureNoteList[i].props.note].adjustX * 2));
      // MeasureNoteList[i].props
      /* rendering the path of the note num */
      Notes.push(
        <G stroke="black" stroke-width="0" fill="black" key={keyvalue++} fillOpacity=".4" fill="red">
          <Path x={[x].join(' ')} y={([y].join(' '))} transform={['scale(', NoteSVG[MeasureNoteList[i].props.note].scale1 * 2, NoteSVG[MeasureNoteList[i].props.note].scale2 * 2, ')'].join(' ')} d={[NoteSVG[MeasureNoteList[i].props.note].data].join(' ')}/>
        </G>
      )
    }
    return Notes;
  }

  checkIntegraty(){
    let check = [];
    fullList[measureNum] = NewMeasureNoteList;
    for (let i = measureNum; i < fullList.length; i++) {
      for (let j = measureNum; j < fullList[i].length; j++) {
        check.push(fullList[i][j]);
      }
    }
    console.log("\n\nDone\n\n");
    console.log(check);
    console.log("\n\n\nNext Phase\n\n\n");
    let NewfullList = [];
    let beats = 0;
    let tempy = [];
    for (let i = measureNum; i < check.length; i++) {
      if(!(check[i].props.note == 0 || check[i].props.note == 6 || check[i].props.note == 7)){
        if(beats == 4){
          NewfullList.push(tempy);
          tempy = [];
          beats = 0;
        } else if(beats > 4){ //Cleff
            this.setState({
              verfColor: "gray",
            });
            console.log("Stopped on measure: " + i);
            return;
        }
        beats += check[i].props.length;
        tempy.push(check[i]);
      }
    }
    this.setState({
      verfColor: "green",
    });
    console.log("\n\n NEW LIST\n\n");
    console.log(NewfullList);
    NewMeasureNoteList.push();
    return;
  }

  verfyButtonPress(){
    this.checkIntegraty();
    // this.setState({
    //   verfColor: "gray",
    // });
    // if(this.state.verfColor == "green"){
    //
    // }
  }

  render(){
    console.log("viewMeasure Render\n");

    // this.checkIntegraty();
    return (
      <View style={styles.container}>
        <Header
          key={keyvalue++}
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
          <Rect x={SCREEN_WIDTH/2 - ((SCREEN_WIDTH/4)/2)} y={SCREEN_HEIGHT - (SCREEN_HEIGHT/4) - ((SCREEN_HEIGHT/15)/2)} width={SCREEN_WIDTH/4} height={SCREEN_HEIGHT/15} rx="15" ry="15" fill={this.state.verfColor} onPress={() => this.verfyButtonPress()} />
          {this.lineSection()}
          {this.NotesEditRender()}
        </Svg>

      </View>
    )
  }
};
// <TouchableOpacity onPress={this.verfyButtonPress() style={styles.VerfButtoncontainer}>
//   <Text
//     stroke="black"
//     fontSize="25"
//     x={[SCREEN_WIDTH / 2].join(' ')}
//     y={[start / 2].join(' ')}
//     textAnchor="middle"
//   >yellow</Text>
// </TouchableOpacity>
  function mapStateToProps(state) {
    return {}
  }

  function mapDispatchToProps(dispatch) {
    return {}
  }

  const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor:"white",
    },
    header: {
      flex: .13,
      backgroundColor: 'black',
    },
    VerfButton: {
      color: 'blue',
      fontWeight: 'bold',
      fontSize: 30,
    },
    VerfButtoncontainer: {
      color: 'blue',
      fontWeight: 'bold',
      fontSize: 30,
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
