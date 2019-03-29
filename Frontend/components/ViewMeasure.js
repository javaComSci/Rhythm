/**
 * importing all the things I need to make this monster.
 * This includes but not limited to, React, react-native, react-redux,
 * react-native-easy-Grid, react-native-vector-icons/AntDesign
 * react-native-pinch-zoom-view, expo, and most importantly SVG.
 */

import React from 'react';
  import { ListItem, Animated, PanResponder, Dimensions,TextInput, Alert, FlatList, TouchableOpacity, ScrollView, StyleSheet, View, KeyboardAvoidingView, Image, ImageBackground, Button as Butt } from 'react-native';
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

var EditScreen = require('./EditMusicScreen');
var NoteSVG = require('./jsons/NotesData.json');
var MiscJson = require('./jsons/EditMisc.json');

var MeasureNoteList = [];
var NewMeasureNoteList;
var fullList = [];
let CIRCLE_RADIUS = 60;
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
    console.log("FEAWFAEWF");
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
      console.log("CONSTRUCTERFF \n");
      console.log(EditScreen.FullListOfNotesArrTrouble);
      fullList = this.props.navigation.getParam('full');
      MeasureNoteList = this.props.navigation.getParam('arr');
      measureNum = this.props.navigation.getParam('num');
      this.state = {
        verfColor: "green",
        showDraggable   : true,
        dropZoneValues  : null,
        pan1             : new Animated.ValueXY(),
        pan2             : new Animated.ValueXY()
      };
      this.panResponder1 = PanResponder.create({
          onStartShouldSetPanResponder: () => true,
          onPanResponderMove: Animated.event([null,{
              dx  : this.state.pan1.x,
              dy  : this.state.pan1.y
          }]),
          onPanResponderRelease: (e, gesture) => {
            console.log("Dropped1");
              if(this.isDropZone(gesture)){
                  this.setState({
                      showDraggable : false
                  });
              }else{
                  Animated.spring(
                      this.state.pan1,
                      {toValue:{x:0,y:0}}
                  ).start();
              }
          }
      });

      this.panResponder2 = PanResponder.create({
          onStartShouldSetPanResponder: () => true,
          onPanResponderMove: Animated.event([null,{
              dx  : this.state.pan2.x,
              dy  : this.state.pan2.y
          }]),
          onPanResponderRelease           : (e, gesture) => {
              if(this.isDropZone(gesture)){
                  this.setState({
                      showDraggable : false
                  });
              }else{
                  Animated.spring(
                      this.state.pan2,
                      {toValue:{x:0,y:0}}
                  ).start();
              }
              console.log("Dropped2");
          }
      });
  }

  static navigationOptions = {
      title: 'Welcome', header: null
  };

  componentDidMount() {
    MeasureNoteList = [];
    fullList = [];
  }

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

  NotesEditRender(notes, color, fill){
    console.log("STARTING NOTESEDITRENDER");
    console.log(notes);
    if (notes.length == 0) {
      console.log("Da fuck?");
      return;
    }
    let s = 0;
    let betweenNotes = (SCREEN_WIDTH/(notes.length+2));
    if(notes[0].props.note == 0 || notes[0].props.note == 6){
      s++;
      betweenNotes = (SCREEN_WIDTH/(notes.length+1));
    }
    let FirstNote = SCREEN_WIDTH/8;
    let halfHeight = SCREEN_HEIGHT/3;
    // halfHeight += SCREEN_HEIGHT/80;
    let start = SCREEN_HEIGHT/8;

    let Notes = [];

    for (var i = s; i < notes.length; i++) {
      let x = FirstNote + (notes[i].props.length * (((i-s) * betweenNotes + (NoteSVG[notes[i].props.note].adjustX * 2))));
      let y = halfHeight + (NoteSVG[notes[i].props.note].adjustY * 2) + (notes[i].props.pitch * SCREEN_HEIGHT/75);
      /* rendering the path of the note num */
      Notes.push(
        <G stroke="black" stroke-width="0" fill="black" key={keyvalue++} fillOpacity={fill} fill={color}>
          <Path x={[x].join(' ')} y={([y].join(' '))} transform={['scale(', NoteSVG[notes[i].props.note].scale1 * 2, NoteSVG[notes[i].props.note].scale2 * 2, ')'].join(' ')} d={[NoteSVG[notes[i].props.note].data].join(' ')}/>
        </G>
      )
    }
    return Notes;
  }

  checkIntegraty(){
    let check = [];
    fullList[measureNum] = NewMeasureNoteList;
    console.log(NewMeasureNoteList);
    for (let i = measureNum; i < fullList.length; i++) {
      for (let j = measureNum; j < fullList[i].length; j++) {
        check.push(fullList[i][j]);
      }
    }
    let NewfullList = [];
    let beats = 0;
    let tempy = [];
    for (let i = measureNum; i < check.length; i++) {
      if(!(check[i].props.note == 0 || check[i].props.note == 6 || check[i].props.note == 7)){
        console.log("beats: " + beats);
        if(beats == 4){
          NewfullList.push(tempy);
          tempy = [];
          beats = 0;
        } else if(beats > 4){ //Cleff
            this.setState({
              verfColor: "gray",
            });
            // NewMeasureNoteList.push(<NoteObjects key={keyvalue++} x={1} y={1} length={.25} note={2} color="black" pitch={1} />);
            return;
        }
        beats += check[i].props.length;
        tempy.push(check[i]);
      }
    }
    this.setState({
      verfColor: "green",
    });
    // console.log("\n\n NEW LIST\n\n");
    // console.log(NewfullList);
    // NewMeasureNoteList.push(<NoteObjects key={keyvalue++} x={1} y={1} length={.25} note={2} color="black" pitch={1} />);
    // NewMeasureNoteList.push(<NoteObjects key={keyvalue++} x={1} y={1} length={1} note={2} color="black" pitch={1} />);
    // NewMeasureNoteList.push(<NoteObjects key={keyvalue++} x={1} y={1} length={1} note={2} color="black" pitch={1} />);
    // NewMeasureNoteList.push(<NoteObjects key={keyvalue++} x={1} y={1} length={1} note={2} color="black" pitch={1} />);
    return;
  }

  verfyButtonPress(){
    NewMeasureNoteList.push(<NoteObjects key={keyvalue++} x={1} y={1} length={1} note={2} color="black" pitch={1} />);
    this.checkIntegraty();
    console.log("PRINTING FULL LIST");
    console.log(fullList);
  }

  onPressEditNote(note){
    console.log(note);
  }

  editNewMeasure(){
    let Notes = [];
    let FirstNote = SCREEN_WIDTH/8;
    let halfHeight = (SCREEN_HEIGHT - (SCREEN_HEIGHT/2.4));
    let betweenNotes = (SCREEN_WIDTH/7);
    let x = FirstNote;
    let y = halfHeight;
    /* rendering the path of the note num */
    return (
      <G stroke="black" stroke-width="0" fill="black" key={keyvalue++} fillOpacity={1} >
        <Path x={[x + (0 * betweenNotes) + (NoteSVG[1].adjustX * 2)].join(' ')} y={([y + (NoteSVG[1].adjustY * 2) + (SCREEN_HEIGHT/140)].join(' '))} transform={['scale(', NoteSVG[1].scale1 * 1.2, NoteSVG[1].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[1].data].join(' ')}/>
        <Rect x={[x + (0 * betweenNotes) + (NoteSVG[1].adjustX * 2) - (SCREEN_WIDTH/40)].join(' ')} y={([y + (NoteSVG[1].adjustY * 2) - (SCREEN_HEIGHT/20)].join(' '))} width={SCREEN_WIDTH/9} height={SCREEN_HEIGHT/15} fillOpacity=".05" onPress={() => this.onPressEditNote(1)}/>
        <Path x={[x + (1 * betweenNotes) + (NoteSVG[2].adjustX * 2)].join(' ')} y={([y + (NoteSVG[2].adjustY * 2) + (SCREEN_HEIGHT/250)].join(' '))} transform={['scale(', NoteSVG[2].scale1 * 1.2, NoteSVG[2].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[2].data].join(' ')}/>
        <Rect x={[x + (1 * betweenNotes) + (NoteSVG[1].adjustX * 2) - (SCREEN_WIDTH/40)].join(' ')} y={([y + (NoteSVG[1].adjustY * 2) - (SCREEN_HEIGHT/20)].join(' '))} width={SCREEN_WIDTH/9} height={SCREEN_HEIGHT/15} fillOpacity=".05" onPress={() => this.onPressEditNote(2)}/>
        <Path x={[x + (2 * betweenNotes) + (NoteSVG[3].adjustX * 2)].join(' ')} y={([y + (NoteSVG[3].adjustY * 2) + (SCREEN_HEIGHT/150)].join(' '))} transform={['scale(', NoteSVG[3].scale1 * 1.2, NoteSVG[3].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[3].data].join(' ')}/>
        <Rect x={[x + (2 * betweenNotes) + (NoteSVG[1].adjustX * 2) - (SCREEN_WIDTH/40)].join(' ')} y={([y + (NoteSVG[1].adjustY * 2) - (SCREEN_HEIGHT/20)].join(' '))} width={SCREEN_WIDTH/9} height={SCREEN_HEIGHT/15} fillOpacity=".05" onPress={() => this.onPressEditNote(3)}/>
        <Path x={[x + (3 * betweenNotes) + (NoteSVG[5].adjustX * 2)].join(' ')} y={([y + (NoteSVG[5].adjustY * 2)].join(' '))} transform={['scale(', NoteSVG[5].scale1 * 1.2, NoteSVG[5].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[5].data].join(' ')}/>
        <Rect x={[x + (3 * betweenNotes) + (NoteSVG[1].adjustX * 2) - (SCREEN_WIDTH/40)].join(' ')} y={([y + (NoteSVG[1].adjustY * 2) - (SCREEN_HEIGHT/20)].join(' '))} width={SCREEN_WIDTH/9} height={SCREEN_HEIGHT/15} fillOpacity=".05" onPress={() => this.onPressEditNote(5)}/>
        <Path x={[x + (4 * betweenNotes) + (NoteSVG[8].adjustX * 2)].join(' ')} y={([y + (NoteSVG[8].adjustY * 2)].join(' '))} transform={['scale(', NoteSVG[8].scale1 * 1.2, NoteSVG[8].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[8].data].join(' ')}/>
        <Rect x={[x + (4 * betweenNotes) + (NoteSVG[1].adjustX * 2) - (SCREEN_WIDTH/40)].join(' ')} y={([y + (NoteSVG[1].adjustY * 2) - (SCREEN_HEIGHT/20)].join(' '))} width={SCREEN_WIDTH/9} height={SCREEN_HEIGHT/15} fillOpacity=".05" onPress={() => this.onPressEditNote(8)}/>
        <Path x={[x + (5 * betweenNotes) + (NoteSVG[9].adjustX * 2)].join(' ')} y={([y + (NoteSVG[9].adjustY * 2)].join(' '))} transform={['scale(', NoteSVG[9].scale1 * 1.2, NoteSVG[9].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[9].data].join(' ')}/>
        <Rect x={[x + (5 * betweenNotes) + (NoteSVG[1].adjustX * 2) - (SCREEN_WIDTH/40)].join(' ')} y={([y + (NoteSVG[1].adjustY * 2) - (SCREEN_HEIGHT/20)].join(' '))} width={SCREEN_WIDTH/9} height={SCREEN_HEIGHT/15} fillOpacity=".05" onPress={() => this.onPressEditNote(9)}/>
        <Path x={[x + (.5 * betweenNotes) + (NoteSVG[10].adjustX * 2)].join(' ')} y={([y + (NoteSVG[10].adjustY * 2) + (SCREEN_HEIGHT/13)].join(' '))} transform={['scale(', NoteSVG[10].scale1 * 1.2, NoteSVG[10].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[10].data].join(' ')}/>
        <Rect x={[x + (.5 * betweenNotes) + (NoteSVG[1].adjustX * 2) - (SCREEN_WIDTH/40)].join(' ')} y={([y + (NoteSVG[1].adjustY * 2) - (SCREEN_HEIGHT/20) + (SCREEN_HEIGHT/13)].join(' '))} width={SCREEN_WIDTH/9} height={SCREEN_HEIGHT/15} fillOpacity=".3" onPress={() => this.onPressEditNote(10)}/>
        <Path x={[x + (1.5 * betweenNotes) + (NoteSVG[11].adjustX * 2)].join(' ')} y={([y + (NoteSVG[11].adjustY * 2)+ (SCREEN_HEIGHT/13)].join(' '))} transform={['scale(', NoteSVG[11].scale1 * 1.2, NoteSVG[11].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[11].data].join(' ')}/>
        <Rect x={[x + (1.5 * betweenNotes) + (NoteSVG[1].adjustX * 2) - (SCREEN_WIDTH/40)].join(' ')} y={([y + (NoteSVG[1].adjustY * 2) - (SCREEN_HEIGHT/20)+ (SCREEN_HEIGHT/13)].join(' '))} width={SCREEN_WIDTH/9} height={SCREEN_HEIGHT/15} fillOpacity=".3" onPress={() => this.onPressEditNote(11)}/>
        <Path x={[x + (2.5 * betweenNotes) + (NoteSVG[12].adjustX * 2)].join(' ')} y={([y + (NoteSVG[12].adjustY * 2)+ (SCREEN_HEIGHT/13)].join(' '))} transform={['scale(', NoteSVG[12].scale1 * 1.2, NoteSVG[12].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[12].data].join(' ')}/>
        <Rect x={[x + (2.5 * betweenNotes) + (NoteSVG[1].adjustX * 2) - (SCREEN_WIDTH/40)].join(' ')} y={([y + (NoteSVG[1].adjustY * 2) - (SCREEN_HEIGHT/20)+ (SCREEN_HEIGHT/13)].join(' '))} width={SCREEN_WIDTH/9} height={SCREEN_HEIGHT/15} fillOpacity=".3" onPress={() => this.onPressEditNote(12)}/>
        <Path x={[x + (3.5 * betweenNotes) + (NoteSVG[13].adjustX * 2)].join(' ')} y={([y + (NoteSVG[13].adjustY * 2)+ (SCREEN_HEIGHT/13)].join(' '))} transform={['scale(', NoteSVG[13].scale1 * 1.2, NoteSVG[13].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[13].data].join(' ')}/>
        <Rect x={[x + (3.5 * betweenNotes) + (NoteSVG[1].adjustX * 2) - (SCREEN_WIDTH/40)].join(' ')} y={([y + (NoteSVG[1].adjustY * 2) - (SCREEN_HEIGHT/20)+ (SCREEN_HEIGHT/13)].join(' '))} width={SCREEN_WIDTH/9} height={SCREEN_HEIGHT/15} fillOpacity=".3" onPress={() => this.onPressEditNote(13)}/>
        <Path x={[x + (4.5 * betweenNotes) + (NoteSVG[14].adjustX * 2)].join(' ')} y={([y + (NoteSVG[14].adjustY * 2)+ (SCREEN_HEIGHT/13)].join(' '))} transform={['scale(', NoteSVG[14].scale1 * 1.2, NoteSVG[14].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[14].data].join(' ')}/>
        <Rect x={[x + (4.5 * betweenNotes) + (NoteSVG[1].adjustX * 2) - (SCREEN_WIDTH/40)].join(' ')} y={([y + (NoteSVG[1].adjustY * 2) - (SCREEN_HEIGHT/20)+ (SCREEN_HEIGHT/13)].join(' '))} width={SCREEN_WIDTH/9} height={SCREEN_HEIGHT/15} fillOpacity=".3" onPress={() => this.onPressEditNote(14)}/>
      </G>
    )
  }

  isDropZone(gesture){
      var dz = this.state.dropZoneValues;
      // return gesture.moveY > dz.y && gesture.moveY < dz.y + dz.height;
      return false;
  }

  setDropZoneValues(event){
      this.setState({
          dropZoneValues : event.nativeEvent.layout
      });
  }

  // renderDraggable2(){
  //     if(this.state.showDraggable){
  //         return (
  //             <View style={{position: 'absolute', top: SCREEN_HEIGHT/2, left: SCREEN_WIDTH/2}}>
  //               <Animated.View
  //                   {...this.panResponder2.panHandlers}
  //                   style={[this.state.pan2.getLayout(),
  //                   {backgroundColor: 'transparent', width: CIRCLE_RADIUS, height: CIRCLE_RADIUS, borderRadius: CIRCLE_RADIUS}]}
  //                   >
  //                   <Svg height="100%"  width="100%">
  //                     <Path x={[CIRCLE_RADIUS/2.8].join(' ')} y={([CIRCLE_RADIUS/1.3].join(' '))} transform={['scale(', NoteSVG[1].scale1 * 1.2, NoteSVG[1].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[1].data].join(' ')}/>
  //                   </Svg>
  //               </Animated.View>
  //             </View>
  //         );
  //     }
  // }

  renderDraggableNotes(locY, locX, note){
      if(this.state.showDraggable){
          return (
              <View style={{position: 'absolute', top: locY, left: locX}}>
                <Animated.View
                    {...this.panResponder1.panHandlers}
                    style={[this.state.pan1.getLayout(),
                    {backgroundColor: 'transparent', width: CIRCLE_RADIUS, height: CIRCLE_RADIUS, borderRadius: CIRCLE_RADIUS}]}
                    >
                    <Svg height="100%"  width="100%">
                      <Path x={[CIRCLE_RADIUS/2.8].join(' ')} y={([CIRCLE_RADIUS/1.3].join(' '))} transform={['scale(', NoteSVG[note].scale1 * 1.2, NoteSVG[note].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[note].data].join(' ')}/>
                    </Svg>
                </Animated.View>
              </View>
          );
      }
  }

  render() {
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
              onPress={() => this.props.navigation.navigate('EditMusicScreen', { arr: fullList })}
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
          {this.NotesEditRender(MeasureNoteList, "gray", .7)}
          {this.NotesEditRender(NewMeasureNoteList, "black", 1)}
        </Svg>

        {this.renderDraggableNotes(SCREEN_HEIGHT/1.7, SCREEN_WIDTH/7, 2)}
        {this.renderDraggableNotes(SCREEN_HEIGHT/1.722, SCREEN_WIDTH/3, 1)}
        {/*this.renderDraggableNotes(SCREEN_HEIGHT/1.7, SCREEN_WIDTH/3, 2)*/}
        {/*this.renderDraggableNotes(SCREEN_HEIGHT/1.7, SCREEN_WIDTH/1, 5)*/}
        {/*this.renderDraggable()*/}

      </View>
    )
  }
};
//http://www.petercollingridge.co.uk/tutorials/svg/interactive/dragging/

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
    dropZone    : {
        height  : SCREEN_HEIGHT/3,
        backgroundColor:'transparent'
    },
    text        : {
        marginTop   : 25,
        marginLeft  : 5,
        marginRight : 5,
        textAlign   : 'center',
        color       : 'black'
    },
    draggableContainer: {
        position    : 'absolute',
        top         : 50,
        left        : 50,
    },
    draggableContainer2: {
      position    : 'absolute',
      top         : 50,
      left        : 50,
    },
    circle      : {
        backgroundColor: 'blue',
        width               : CIRCLE_RADIUS*2,
        height              : CIRCLE_RADIUS*2,
        borderRadius        : CIRCLE_RADIUS
    },
    circle2      : {
        backgroundColor: 'yellow',
        width               : CIRCLE_RADIUS,
        height              : CIRCLE_RADIUS,
        borderRadius        : CIRCLE_RADIUS
    }
  });

  export default connect(mapStateToProps, mapDispatchToProps)(ViewMeasure);


// import React,{ Component } from 'react';
// import { connect } from 'react-redux';
// import {
//     StyleSheet,
//     View,
//     PanResponder,
//     Animated,
//     Easing,
//     Dimensions
// } from 'react-native';

// import { Svg } from 'expo';
// const { Circle, Rect, Path, Line, G, Defs, Use } = Svg;

// const SCREEN_WIDTH = Dimensions.get('window').width
// const SCREEN_HEIGHT = Dimensions.get('window').height
// let CIRCLE_RADIUS = 100;

// var NoteSVG = require('./jsons/NotesData.json');
// var MiscJson = require('./jsons/EditMisc.json');

// class ViewMeasure extends Component{
    // constructor(props){
    //     super(props);
    //
    //     this.state = {
    //         showDraggable   : true,
    //         dropZoneValues  : null,
    //         pan             : new Animated.ValueXY()
    //     };

        // this.panResponder = PanResponder.create({
        //     onStartShouldSetPanResponder    : () => true,
        //     onPanResponderMove              : Animated.event([null,{
        //         dx  : this.state.pan.x,
        //         dy  : this.state.pan.y
        //     }]),
        //     onPanResponderRelease           : (e, gesture) => {
        //         if(this.isDropZone(gesture)){
        //             this.setState({
        //                 showDraggable : false
        //             });
        //         }else{
        //             Animated.spring(
        //                 this.state.pan,
        //                 {toValue:{x:0,y:0}}
        //             ).start();
        //         }
        //     }
        // });
    // }
    //   static navigationOptions = {
    //       title: 'Welcome', header: null
    //   };


    // isDropZone(gesture){
    //     var dz = this.state.dropZoneValues;
    //     return gesture.moveY > dz.y && gesture.moveY < dz.y + dz.height;
    // }
    //
    // setDropZoneValues(event){
    //     this.setState({
    //         dropZoneValues : event.nativeEvent.layout
    //     });
    // }
    // <G stroke="black" stroke-width="0" fill="black" key={keyvalue++} fillOpacity={1} >
// <Rect x={[x + (0 * betweenNotes) + (NoteSVG[1].adjustX * 2) - (SCREEN_WIDTH/40)].join(' ')} y={([y + (NoteSVG[1].adjustY * 2) - (SCREEN_HEIGHT/20)].join(' '))} width={SCREEN_WIDTH/9} height={SCREEN_HEIGHT/15} fillOpacity=".3" onPress={() => this.onPressEditNote(1)}/>
  // </G>
    // render(){
    //     return (
    //         <View style={styles.mainContainer}>
    //             <View
    //                 onLayout={this.setDropZoneValues.bind(this)}
    //                 style={styles.dropZone}>
    //                 <Text style={styles.text}>Drop me here!</Text>
    //             </View>
    //             {/*this.renderDraggable()*/}
    //             {this.renderDraggable2()}
    //         </View>
    //     );
    // }
    // <Svg height="100%"  width="100%">
    //   <Path x={[50].join(' ')} y={([50].join(' '))} transform={['scale(', NoteSVG[1].scale1 * 1.2, NoteSVG[1].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[1].data].join(' ')}/>
    // </Svg>
    // renderDraggable(){
    //     if(this.state.showDraggable){
    //         return (
    //             <View style={styles.draggableContainer}>
    //                 <Animated.View
    //                     {...this.panResponder.panHandlers}
    //
    //                     style={[this.state.pan.getLayout(),
    //                       styles.circle
    //                     ]}>
    //
    //
    //                 </Animated.View>
    //             </View>
    //         );
    //     }
    // }
    // renderDraggable2(){
    //     if(this.state.showDraggable){
    //         return (
    //             <View style={styles.draggableContainer2}>
    //                 <Animated.View
    //                     {...this.panResponder.panHandlers}
    //                     style={[this.state.pan.getLayout(),
    //                     {backgroundColor: 'yellow', width: CIRCLE_RADIUS, height: CIRCLE_RADIUS, borderRadius: CIRCLE_RADIUS}]}
    //                     >
    //                     <Svg height="100%"  width="100%">
    //                       <Path x={[50].join(' ')} y={([50].join(' '))} transform={['scale(', NoteSVG[1].scale1 * 1.2, NoteSVG[1].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[1].data].join(' ')}/>
    //                     </Svg>
    //                 </Animated.View>
    //             </View>
    //         );
    //     }
    // }
// }
//
// function mapStateToProps(state) {}
//
// function mapDispatchToProps(dispatch) {}



// let Window = Dimensions.get('window');
// let styles = StyleSheet.create({
//     mainContainer: {
//         flex    : 1
//     },
//     dropZone    : {
//         height  : SCREEN_HEIGHT/3,
//         backgroundColor:'transparent'
//     },
//     text        : {
//         marginTop   : 25,
//         marginLeft  : 5,
//         marginRight : 5,
//         textAlign   : 'center',
//         color       : 'black'
//     },
//     draggableContainer: {
//         position    : 'absolute',
//         top         : 50,
//         left        : 50,
//     },
//     draggableContainer2: {
//         position    : 'absolute',
//         top         : SCREEN_HEIGHT,
//         left        : 50,
//     },
//     circle      : {
//         backgroundColor: 'blue',
//         width               : CIRCLE_RADIUS*2,
//         height              : CIRCLE_RADIUS*2,
//         borderRadius        : CIRCLE_RADIUS
//     },
//     circle2      : {
//         backgroundColor: 'yellow',
//         width               : CIRCLE_RADIUS,
//         height              : CIRCLE_RADIUS,
//         borderRadius        : CIRCLE_RADIUS
//     }
// });

// export default connect(mapStateToProps, mapDispatchToProps)(ViewMeasure);
