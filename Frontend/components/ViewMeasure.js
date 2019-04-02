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
  import NoteObjects from './NotesObjects'

const SCREEN_WIDTH = Dimensions.get('window').width
const SCREEN_HEIGHT = Dimensions.get('window').height

var EditScreen = require('./EditMusicScreen');
var NoteSVG = require('./jsons/NotesData.json');
var MiscJson = require('./jsons/EditMisc.json');

var MeasureNoteList = [];
var NewMeasureNoteList;
var fullList = [];
let CIRCLE_RADIUS = SCREEN_WIDTH/6;
var measureNum;
var panHandlers = [];
var clickedX = -1;
var clickedY = -1;
var hasClef;
var draggables = [];

var keyvalue;


class ViewMeasure extends React.Component {

  constructor(props) {
      super(props);
      draggables = [];
      panHandlers = [];
      NewMeasureNoteList = [];
      keyvalue = 0;
      fullList = [];

      draggables.push(
        [SCREEN_HEIGHT/1.6, SCREEN_WIDTH/7, 5, keyvalue++]
      );
      draggables.push(
        [SCREEN_HEIGHT/1.6, SCREEN_WIDTH/3, 1, keyvalue++]
      );
      draggables.push(
        [SCREEN_HEIGHT/1.6, SCREEN_WIDTH/2, 2, keyvalue++]
      );
      draggables.push(
        [SCREEN_HEIGHT/1.6, SCREEN_WIDTH/1.5, 3, keyvalue++]
      );

      /* Grabbing the params sent through React Navigation */
      fullList = this.props.navigation.getParam('full');
      MeasureNoteList = this.props.navigation.getParam('arr');
      measureNum = this.props.navigation.getParam('num');

      console.log("fullList");
      console.log(fullList);

      console.log("\n\nMeasureNoteList");
      console.log(MeasureNoteList);

      console.log("\n\nmeasureNum " + measureNum);

      if(MeasureNoteList.length != 0){
        if((MeasureNoteList[0].props.note == 0 || MeasureNoteList[0].props.note == 6 || MeasureNoteList[0].props.note == 7)){
          hasClef = MeasureNoteList[0].props.note;
          MeasureNoteList.splice(0,1);
        }else{
          hasClef = -1;
        }
      }else{
        hasClef = -1;
        MeasureNoteList = [];
      }

      this.state = {
        verfColor: "green",
        showDraggable   : true,
        dropZoneValues  : null,
        panLayouts: [],
      };

      this.state.panLayouts = [];


      /* This for loop sents up all the drag and drops.. This code is jank AF */
      for (let i = 0; i < 50; i++) {
        this.state.panLayouts.push(new Animated.ValueXY());
        panHandlers.push(
          this.panResponder2 = PanResponder.create({
              onStartShouldSetPanResponder: (e, gesture) => {
                // console.log("clicked");
                clickedY = e.nativeEvent.locationY;
                clickedX = e.nativeEvent.locationX;
                // console.log(e.nativeEvent.pageX + " : " + e.nativeEvent.pageY);
                // console.log(this.state.panLayouts[i]);
                // this.state.panLayouts[i].setValue({
                //   x: e.nativeEvent.pageX, y: e.nativeEvent.pageY
                // })
                return true;

              },
              onPanResponderMove: (e, gesture) => {
                // console.log("before");
                // console.log(this.state.panLayouts[i]);
                // console.log("moved");
                if(this.checkDropBoxes(e.nativeEvent.pageX, e.nativeEvent.pageY, i, (e.nativeEvent.pageX - gesture.dx), (e.nativeEvent.pageY - gesture.dy), gesture, e) == -1){

                  this.state.panLayouts[i].setValue({
                    x: gesture.dx, y: gesture.dy
                  })

                }
                // console.log("after");
                // console.log(this.state.panLayouts[i]);
              },
              onPanResponderRelease: (e, gesture) => {
                // console.log("realsed");
                // console.log(draggables);
                // draggables[i][0] += (gesture.y0);
                let check = this.checkDropBoxes(e.nativeEvent.pageX, e.nativeEvent.pageY, i, (e.nativeEvent.pageX - gesture.dx), (e.nativeEvent.pageY - gesture.dy), gesture, e)
                  if(check != -1){

                    switch (draggables[i][2]) {
                      case 5:
                        NewMeasureNoteList.push({
                          props: {
                            note: 5,
                            length: .25,
                            pitch: (check % 11),
                            x: Math.floor(check / 11),
                          }
                        });
                        // NewMeasureNoteList.push(<NoteObjects key={keyvalue++} x={Math.floor(check / 11)} y={this.props.navigation.getParam('yValue')} length={.25} note={5} color="black" pitch={(check % 11)} />);
                        draggables.push(
                          [SCREEN_HEIGHT/1.6, SCREEN_WIDTH/7, 5]
                        );
                        // draggables.push(
                        //   [SCREEN_HEIGHT/1.6 + gesture.y0, SCREEN_WIDTH/7 + gesture.x0, 5]
                        // );
                        break;
                      case 1:
                        draggables.push(
                          [SCREEN_HEIGHT/1.6, SCREEN_WIDTH/3, 1, keyvalue++]
                        );
                        NewMeasureNoteList.push({
                          props: {
                            note: 1,
                            length: .5,
                            pitch: (check % 11),
                            x: Math.floor(check / 11),
                          }
                        });
                        // NewMeasureNoteList.push(<NoteObjects key={keyvalue++} x={Math.floor(check / 11)} y={this.props.navigation.getParam('yValue')} length={.5} note={1} color="black" pitch={(check % 11)} />);
                        break;
                      case 2:
                        draggables.push(
                          [SCREEN_HEIGHT/1.6, SCREEN_WIDTH/2, 2, keyvalue++]
                        );
                        NewMeasureNoteList.push({
                          props: {
                            note: 2,
                            length: 1,
                            pitch: (check % 11),
                            x: Math.floor(check / 11),
                          }
                        });
                        // NewMeasureNoteList.push(<NoteObjects key={keyvalue++} x={Math.floor(check / 11)} y={this.props.navigation.getParam('yValue')} length={1} note={2} color="black" pitch={(check % 11)} />);
                        break;
                      case 3:
                        draggables.push(
                          [SCREEN_HEIGHT/1.6, SCREEN_WIDTH/1.5, 3, keyvalue++]
                        );
                        NewMeasureNoteList.push({
                          props: {
                            note: 3,
                            length: 2,
                            pitch: (check % 11),
                            x: Math.floor(check / 11),
                          }
                        });
                        // NewMeasureNoteList.push(<NoteObjects key={keyvalue++} x={Math.floor(check / 11)} y={this.props.navigation.getParam('yValue')} length={2} note={3} color="black" pitch={(check % 11)} />);
                        break;
                      case 4:
                        // draggables.push(
                        //   [SCREEN_HEIGHT/1.6, SCREEN_WIDTH/1.5, 3, keyvalue++]
                        // );
                        break;
                      case 5:
                        // draggables.push(
                        //   [SCREEN_HEIGHT/1.6, SCREEN_WIDTH/1.5, 3, keyvalue++]
                        // );
                        break;
                    case 6:
                      // draggables.push(
                      //   [SCREEN_HEIGHT/1.6, SCREEN_WIDTH/1.5, 3, keyvalue++]
                      // );
                      break;
                    }

                  }else{
                      Animated.spring(
                          this.state.panLayouts[i],
                          {toValue:{x:0,y:0}}
                      ).start();
                  }
                  // console.log(NewMeasureNoteList);
                  // console.log(draggables);
                  this.setState({ });


              }
        }))
      }
  }

  static navigationOptions = {
      title: 'Welcome', header: null
  };

  componentDidMount() {
    /* resetting all global values */
    // MeasureNoteList = [];
    // // panHandlers = [];
    // fullList = [];
    // NewMeasureNoteList = [];
  }

  componentWillMount() {
    /* Not sure what this does but its needed */
    // NewMeasureNoteList = [];
  }

  newLineSection(){
    let newLines = [];
    for (let i = 0; i < 5; i++) {
      newLines.push(
        <Line
            x1={SCREEN_WIDTH/10}
            y1={SCREEN_HEIGHT/3.5 + (i * SCREEN_HEIGHT/25)}
            x2={9*SCREEN_WIDTH/10}
            y2={SCREEN_HEIGHT/3.5 + (i * SCREEN_HEIGHT/25)}
            stroke="black"
            strokeWidth="2"
        />
      )
    }
      for (let i = 0; i < 2; i++) {
        newLines.push(
          <Line
              x1={SCREEN_WIDTH/10 + (i * (8 * SCREEN_WIDTH/10))}
              y1={SCREEN_HEIGHT/3.51}
              x2={SCREEN_WIDTH/10  + (i * (8 * SCREEN_WIDTH/10))}
              y2={SCREEN_HEIGHT/2.24}
              stroke="black"
              strokeWidth="2"
          />
        )
    }
    return (
      newLines
    )
  }

  NotesEditRender(notes, color, fill){
    // console.log("STARTING NOTESEDITRENDER");
    // console.log(notes);
    if (notes.length == 0) {
      return;
    }
    let s = 0;

    let Notes = [];

    for (var i = s; i < notes.length; i++) {
      // let x = FirstNote + (notes[i].props.length * (((i-s) * betweenNotes + (NoteSVG[notes[i].props.note].adjustX * 2))));
      // let y = halfHeight + (NoteSVG[notes[i].props.note].adjustY * 2) + (notes[i].props.pitch * SCREEN_HEIGHT/75);
      let x = (SCREEN_WIDTH/8) + (NoteSVG[notes[i].props.note].adjustX * 1.8);
      let y = 250;
      /* rendering the path of the note num */
      Notes.push(
        <G stroke="black" stroke-width="0" fill="black" key={keyvalue++} fillOpacity={fill} fill={color}>
          <Path x={[x].join(' ')} y={([y].join(' '))} transform={['scale(', NoteSVG[notes[i].props.note].scale1 * 1.2, NoteSVG[notes[i].props.note].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[notes[i].props.note].data].join(' ')}/>
        </G>
      )
    }
    return Notes;
  }

  checkIntegraty(checker){
    let check = [];
    // fullList[measureNum] = check;
    // console.log(NewMeasureNoteList);
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
        // console.log("beats: " + beats);
        if(beats == 4){
          NewfullList.push(tempy);
          tempy = [];
          beats = 0;
        } else if(beats > 4){ //Cleff
            this.setState({
              verfColor: "gray",
            });
            // NewMeasureNoteList.push(<NoteObjects key={keyvalue++} x={1} y={1} length={.25} note={2} color="black" pitch={1} />);
            return false;
        }
        beats += check[i].props.length;
        tempy.push(check[i]);
      }
    }
    this.setState({
      verfColor: "green",
    });
    return true;
  }

  verfyButtonPress(){
    let sendupdated = [];
    // if(NewMeasureNoteList.length == 0){
    //   fullList.splice(measureNum, measureNum+1);
    //   console.log(fullList);
    //   this.props.navigation.navigate('EditMusicScreen', { arr: fullList, cleff: this.props.navigation.getParam('cleff')})
    // }
    if(hasClef != -1){
      // NewMeasureNoteList.unshift({
      //   props: {
      //     note: hasClef,
      //     length: 0,
      //     pitch: 1,
      //     x: 1,
      //   }
      // });
    }
    console.log("measureNum: " + measureNum);
    fullList[measureNum] = NewMeasureNoteList;
    let newFullList = [];
    for (let i = 0; i < fullList.length; i++) {
      for (let j = 0; j < fullList[i].length; j++) {
        newFullList.push(fullList[i][j]);
      }
    }



    let beats = 0;
    let tempy = [];
    let sendFullList = [];
    let measure = 0;
    let oldbeat = 0;
    let addmesure = 0;
    if(this.props.navigation.getParam('sheetType') == 1){
      addmesure = 2;
    }
    // console.log(newFullList);
    tempy.push(<NoteObjects key={keyvalue++} x={1} y={Math.ceil((measure/2) + .01)} length={0} note={0} color="black" pitch={1} />);
    for (let i = 0; i < newFullList.length; i++) {
      if(!(newFullList[i].props.note == 0 || newFullList[i].props.note == 6 || newFullList[i].props.note == 7)){
        // console.log(newFullList[i].props.length);
        beats += newFullList[i].props.length;
        // console.log("Beats: " + beats);
        if(beats > 4){
          // console.log("TEMPY");
          // console.log(tempy);
          sendFullList.push(tempy);
          tempy = [];
          beats = newFullList[i].props.length;
          measure++;
          if(measure%2 == 0){
            measure += addmesure;
            tempy.push(<NoteObjects key={keyvalue++} x={1} y={Math.ceil((measure/2) + .01)} length={0} note={0} color="black" pitch={1} />);
          }
        }
        // console.log("beats: " + beats);
        tempy.push(<NoteObjects key={keyvalue++} x={2 + (beats - newFullList[i].props.length) + (4*(measure%2))} y={Math.ceil((measure/2) + .01)} length={newFullList[i].props.length} note={newFullList[i].props.note} color="black" pitch={newFullList[i].props.pitch} />);
        // oldbeat = troubleCleff[i].length;
      }
    }
    if(tempy.length != 0){
      sendFullList.push(tempy);
      // console.log(tempy);
    }

    console.log("sendFillList");
    console.log(sendFullList);
    // console.log("FEAWFEAWFEWA");
    // console.log(sendFullList);

    // console.log("SENDING");
    // console.log(sendFullList);
    // console.log("\n\n\n\n\n\n\n");
    // console.log(fullList);

    this.props.navigation.navigate('EditMusicScreen', { arr: sendFullList, cleff: this.props.navigation.getParam('cleff')})
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

  isDropZone(x,y){
    // console.log("x: " + x);
    // console.log("y: " + y);
    return false;
  }

  checkDropBoxes(x, y, i, offsetX, offsetY, g, e){
    for (let j = 0; j < 16; j++) {
        for (let k = 0; k < 11; k++) {

        let a = x - (SCREEN_WIDTH/8) - (j * SCREEN_WIDTH/20);
        let b = y - ((SCREEN_HEIGHT/3.5) + (SCREEN_HEIGHT/20) + CIRCLE_RADIUS/2 + (((k+1) * SCREEN_HEIGHT / 25))/2 - SCREEN_HEIGHT/50);
        let dist = Math.sqrt(a*a + b*b);

        if(dist < 13) {
          // console.log("g.x0 - clickedX = " + (g.x0 - clickedX));
          // console.log("g.y0 - clickedY = " + (g.y0 - clickedY));
          this.state.panLayouts[i].setValue({
            x: (SCREEN_WIDTH/8 - (g.x0 - clickedX) - CIRCLE_RADIUS/2 + (j * SCREEN_WIDTH/20)),
            y: (((SCREEN_HEIGHT/3.5) + (SCREEN_HEIGHT/25)) - (g.y0 - clickedY) + (((k+1) * SCREEN_HEIGHT / 25))/2 - SCREEN_HEIGHT/50)
          })
          // console.log("inside");
          // console.log(this.state.panLayouts[i]);
          return ((11*j) + k);
        }
      }
    }
    return -1;
  }

  DropZonerendering(){
    // console.log(e.nativeEvent.pageX);
    // console.log(e.nativeEvent.pageY);
    let renderBoxes = [];
    let fillColor = "blue";
    for (let i = 0; i < 16; i++) {
      if(i == 15){
        fillColor = "red";
      }
      for (let j = 0; j < 11; j++) {
        // console.log(SCREEN_WIDTH/8 + (i * SCREEN_WIDTH/20));
        // console.log(((SCREEN_HEIGHT/3.5) + ((j * SCREEN_HEIGHT / 25))/2) - SCREEN_HEIGHT/50);
        renderBoxes.push(
          <Circle
            cx={SCREEN_WIDTH/8 + (i * SCREEN_WIDTH/20)}
            cy={((SCREEN_HEIGHT/3.5) + (((j) * SCREEN_HEIGHT / 25))/2) - SCREEN_HEIGHT/50}
            r={3}
            fill={fillColor}
            fillOpacity=".5"
            strokeWidth="0"
          />
        )
      }
    }
    return renderBoxes;
  }

  renderDraggableNotes(drags){
    // console.log("i: "+ i);
    // console.log(drags);
      if(this.state.showDraggable){
        let ret = [];
        for (let i = 0; i < drags.length; i++) {
          ret.push(
            <View style={{position: 'absolute', top: drags[i][0], left: drags[i][1]}}>
              <Animated.View
                  {...panHandlers[i].panHandlers}
                  style={[this.state.panLayouts[i].getLayout(),
                  {backgroundColor: 'transparent', width: CIRCLE_RADIUS, height: CIRCLE_RADIUS, borderRadius: CIRCLE_RADIUS}]}
                  >
                  <Svg height="100%"  width="100%">
                    <Path x={[CIRCLE_RADIUS/2.8 + (NoteSVG[drags[i][2]].adjustX)].join(' ')} y={([CIRCLE_RADIUS/1.3 + (NoteSVG[drags[i][2]].adjustY)].join(' '))} transform={['scale(', NoteSVG[drags[i][2]].scale1 * 1.2, NoteSVG[drags[i][2]].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[drags[i][2]].data].join(' ')}/>
                  </Svg>
              </Animated.View>
            </View>
          )
        }
        return ret;
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
              onPress={() => this.props.navigation.navigate('EditMusicScreen', { arr: [] })}
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
          {/*this.lineSection()*/}
          {this.newLineSection()}
          {/*this.NotesEditRender(MeasureNoteList, "gray", .7)*/}
          {/*this.NotesEditRender(NewMeasureNoteList, "black", 1)*/}
          {this.DropZonerendering()}
        </Svg>
        {this.renderDraggableNotes(draggables)}


        {/*this.renderDraggable()*/}

      </View>
    )
  }
};
// {this.renderDraggableNotes(SCREEN_HEIGHT/1.68, SCREEN_WIDTH/7, 5, 0)}
// {this.renderDraggableNotes(SCREEN_HEIGHT/1.718, SCREEN_WIDTH/3, 1, 1)}
// {this.renderDraggableNotes(SCREEN_HEIGHT/1.7, SCREEN_WIDTH/2, 2, 2)}
// {this.renderDraggableNotes(SCREEN_HEIGHT/1.713, SCREEN_WIDTH/1.5, 3, 3)}
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





//
//
// import React,{ Component } from 'react';
// import { connect } from 'react-redux';
// import {
//     StyleSheet,
//     View,
//     PanResponder,
//     Animated,
//     Easing,
//     Dimensions,
//     Text
// } from 'react-native';
//
// import { Svg } from 'expo';
// const { Circle, Rect, Path, Line, G, Defs, Use } = Svg;
//
// const SCREEN_WIDTH = Dimensions.get('window').width
// const SCREEN_HEIGHT = Dimensions.get('window').height
// let CIRCLE_RADIUS = 100;
//
// var NoteSVG = require('./jsons/NotesData.json');
// var MiscJson = require('./jsons/EditMisc.json');
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
//       static navigationOptions = {
//           title: 'Welcome', header: null
//       };
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
// //     <G stroke="black" stroke-width="0" fill="black" key={keyvalue++} fillOpacity={1} >
// // <Rect x={[x + (0 * betweenNotes) + (NoteSVG[1].adjustX * 2) - (SCREEN_WIDTH/40)].join(' ')} y={([y + (NoteSVG[1].adjustY * 2) - (SCREEN_HEIGHT/20)].join(' '))} width={SCREEN_WIDTH/9} height={SCREEN_HEIGHT/15} fillOpacity=".3" onPress={() => this.onPressEditNote(1)}/>
// //   </G>
//     render(){
//         return (
//             <View style={styles.mainContainer}>
//                 <View
//                     onLayout={this.setDropZoneValues.bind(this)}
//                     style={styles.dropZone}>
//                     <Text style={styles.text}>Drop me here!</Text>
//                 </View>
//                 {/*this.renderDraggable()*/}
//                 {this.renderDraggable2()}
//             </View>
//         );
//     }
//     // <Svg height="100%"  width="100%">
//     //   <Path x={[50].join(' ')} y={([50].join(' '))} transform={['scale(', NoteSVG[1].scale1 * 1.2, NoteSVG[1].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[1].data].join(' ')}/>
//     // </Svg>
//     renderDraggable(){
//         if(this.state.showDraggable){
//             return (
//                 <View style={styles.draggableContainer}>
//                     <Animated.View
//                         {...this.panResponder.panHandlers}
//
//                         style={[this.state.pan.getLayout(),
//                           styles.circle
//                         ]}>
//
//
//                     </Animated.View>
//                 </View>
//             );
//         }
//     }
//     renderDraggable2(){
//         if(this.state.showDraggable){
//             return (
//                 <View style={styles.draggableContainer2}>
//                     <Animated.View
//                         {...this.panResponder.panHandlers}
//                         style={[this.state.pan.getLayout(),
//                         {backgroundColor: 'yellow', width: CIRCLE_RADIUS, height: CIRCLE_RADIUS, borderRadius: CIRCLE_RADIUS}]}
//                         >
//                         <Svg height="100%"  width="100%">
//                           <Path x={[50].join(' ')} y={([50].join(' '))} transform={['scale(', NoteSVG[1].scale1 * 1.2, NoteSVG[1].scale2 * 1.2, ')'].join(' ')} d={[NoteSVG[1].data].join(' ')}/>
//                         </Svg>
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
//
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
//
// export default connect(mapStateToProps, mapDispatchToProps)(ViewMeasure);
