/**
 * importing all the things I need to make this monster.
 * This includes but not limited to, React, react-native, react-redux,
 * react-native-easy-Grid, react-native-vector-icons/AntDesign
 * react-native-pinch-zoom-view, expo, and most importantly SVG.
 */


// list of instruments and clefs
// Both: piano and harp
// Treble: violin, flute, guitar
// Bass: tuba, cello, Bass
// Alto: trombone, viola



import React from 'react';
import { ListItem, Dimensions, TextInput, Alert, FlatList, TouchableOpacity, ScrollView, StyleSheet, View, KeyboardAvoidingView, Image, ImageBackground } from 'react-native';
// import { Header } from 'react-navigation';
import { connect } from 'react-redux';
import { Button, Header } from 'react-native-elements';
import { Col, Row, Grid } from "react-native-easy-grid";
import Icon from 'react-native-vector-icons/AntDesign'
import IconMaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons'
import PinchZoomView from 'react-native-pinch-zoom-view';
import NoteObjects from './NotesObjects'

import { Svg } from 'expo';
const { Circle, Rect, Path, Line, Text, G, Defs, Use } = Svg;

/* Icon used from here for back button, this might be taken away */
// https://oblador.github.io/react-native-vector-icons/

// var sampleJson = require('./testRichard.json');
// var sampleJson = require('./SampleMusicSheet.json');
var NoteSVG = require('./jsons/NotesData.json');
var MiscJson = require('./jsons/EditMisc.json');

var sampleJson = require('./jsons/MusicSheet0.json');

var sampleJson0 = require('./jsons/MusicSheet0.json');
var sampleJson1 = require('./jsons/MusicSheet1.json');
var sampleJson2 = require('./jsons/MusicSheet2.json');
var sampleJson3 = require('./jsons/MuiscSheet32Hands.json');
var sampleJson4 = require('./jsons/MusicSheet3.json');
var sampleJson4 = require('./jsons/test1.json');
// var sampleJson3 = require('./jsons/MuiscSheet32Hands.json');
// var sampleJson3 = require('./MusicSheet3.json');
// var sampleJson = require('./SampleMusicSheet.json');
// var sampleJson = require('./SampleMusicSheet.json');

// var NotesList = [];
//
// var NotesListByMeasure = [];
// var ran1 = [0,5,10,15,20,25,30,35,40,45,50,55]

// var styles = require('../style');

/* getting the dims of the screen that is accessing this code */
const SCREEN_WIDTH = Dimensions.get('window').width
const SCREEN_HEIGHT = Dimensions.get('window').height

/* this is the total amount of beats in the music sheet currently */
var totalBeats = 0;

/* Setting a varible for the screen_height that can be modified */
var screenSize = SCREEN_HEIGHT;
/* how far to make the screen go down */
var screenExtendSize = 0;

var CleffLines;

var troubleCleffSplit = [];
var baseCleffSplit = [];
var altoCleffSplit = [];

var keyvalue;

var firstRender = 1;

/* This is the sheet id to update */
var sheet_id;

var forceRender = true;

/*
 * This is the Component that holds all the notes and
 * renders each note depending on the note num, pitch, and length
 */


class EditMusicScreen extends React.Component {

  constructor(props) {
    super(props);
    firstRender = 1;
    // troubleCleffSplit  = [];
    // troubleCleff = [];
    console.log("Constructor");
    console.log(props.navigation.getParam('arr'));
    // if(this.props.navigation.getParam('arr') != undefined){
    //   console.log("pma");
    // }
    /* grabbing the file from the backend */
    sampleJson = props.navigation.getParam('file')
    sheet_id = props.navigation.getParam('sheet_id')
    console.log("sheet_id = " + sheet_id);
    // fetch("http://68.183.140.180:5000/getInfoBySheetID",
    // {
    //   method: 'POST',
    //   headers: {
    //       Accept: 'application/json',
    //       'Content-Type': 'application/json',
    //   },
    //   body: JSON.stringify({
    //     "table": "sheet_music",
    //     "id": sheet_id
    //   }),
    // }).then(result => {
    //     result.text().then(res => {
    //         console.log("res", res)
    //         sampleJson = res[0][0];
    //     }).catch(err => {
    //         console.log("err", err)
    //     })
    // });

    console.log("This is the file being passed ");
    console.log(sampleJson);
    // Set it as an empty json is null;
    if (sampleJson == null) {
      sampleJson = {
        "clef": 0,
        "notes":
          [
            {
              "note": 0,
              "length": 0,
              "pitch": 1
            },
            {
              "note": 6,
              "length": 0,
              "pitch": 1
            }
          ]
      }
    }
    // sampleJson = sampleJson0;

    ids = [];
    ids.push(this.props.navigation.getParam('sheet_id'));

    console.log("IN THE EDIT SHEET SCREEN " + this.props.navigation.getParam('sheet_id'));

    this.state = {
      colorProp: 'black',
      alert: false,
      SheetType: 0,
      troubleCleff: troubleCleffSplit,
      baseCleff: baseCleffSplit,
      sheet_ids: ids,
      email: this.props.navigation.getParam('email'),
    };
  }

  static navigationOptions = {
    title: 'Welcome', header: null
  };

  componentDidMount() {
    console.log("componentDidMount");
  }

  componentWillMount() {
    console.log("Component will mount!")
    let Extrarows = 0;
    screenExtendSize = 0;
    totalBeats = 0;
    // for (let i = 0; i < sampleJson.notes.length; i++) {
    for (let i = 0; i < sampleJson.notes.length; i++) {
      Extrarows += sampleJson.notes[i].length
      totalBeats += sampleJson.notes[i].length;
      // NotesList.push(<NoteObjects _id={i} note={sampleJson.notes[i].note} len={sampleJson.notes[i].length} pitch={sampleJson.notes[i].pitch} color="black" />);
    }
    screenExtendSize += ((Math.ceil(Extrarows / 8) - 7) * SCREEN_HEIGHT / 9);
    if (screenExtendSize < 0) {
      screenExtendSize = 0;
    }
    if(this.state.SheetType == 1)
      screenExtendSize+=SCREEN_HEIGHT / 9;
  }

  setTitle(title) {
    let start = SCREEN_HEIGHT / 8;
    return (
      <Svg height="100%" width="100%">
        <Text
          stroke="black"
          fontSize="25"
          x={[SCREEN_WIDTH / 2].join(' ')}
          y={[start / 2].join(' ')}
          textAnchor="middle"
        >{title}</Text>
      </Svg>
    )
  }

  placeVerticalLines(line) {
    let mesureLength = SCREEN_WIDTH / 10;
    let start = SCREEN_HEIGHT / 8;
    start *= line
    return (
      <Svg height="100%" width="100%">
        {this.VerticalSection(mesureLength, start)}
        {this.VerticalSection(mesureLength * 5.25, start)}
        {this.VerticalSection(mesureLength * 9.05, start)}
      </Svg>
    )
  }

  lineSection() {
    // console.log(totalBeats);
    let Measures = [];
    let spaceBetween = SCREEN_HEIGHT / 82;
    let mesureLength = SCREEN_WIDTH / 10;
    let start = SCREEN_HEIGHT / 8;
    let betweenNotes = SCREEN_WIDTH / 11;
    let Rows = Math.max(troubleCleffSplit.length, baseCleffSplit.length, altoCleffSplit.length);
    if(Rows % 2 == 0){
      Rows++;
    }
    Rows = Rows/2;
    // Rows++;

    // if(Rows == 0)
    //   Rows++;

    if(this.state.SheetType == 0){
      for (let i = 0; i < Rows; i++) {
        Measures.push(
          <G height="100%" width="100%" key={keyvalue++}>
            <Path x={[mesureLength].join(' ')} y={[(i + 1) * start].join(' ')} transform={['scale(', mesureLength / 25, spaceBetween / 24.5, ')'].join(' ')} style="fill:green"
              d={[MiscJson[0].data].join(' ')} />
            {this.VerticalSection(mesureLength, start * (i + 1))}
            {this.VerticalSection(mesureLength * 9, start * (i + 1))}
            {this.VerticalSection(mesureLength * 5.3, start * (i + 1))}
            {/*this.renderMeasureBoxes(i,0)*/}
            {/*this.renderMeasureBoxes(i,1)*/}
          </G>
        )
      }
    }

    if(this.state.SheetType == 1){
      Rows++;
      for (let i = 0; i < Rows*2; i++) {
        Measures.push(
          <G height="100%" width="100%" key={keyvalue++}>
            <Path x={[mesureLength].join(' ')} y={[(i + 1) * start].join(' ')} transform={['scale(', mesureLength / 25, spaceBetween / 24.5, ')'].join(' ')} style="fill:green"
              d={[MiscJson[0].data].join(' ')} />
            {this.VerticalSection(mesureLength, start * (i + 1))}
            {this.VerticalSection(mesureLength * 9, start * (i + 1))}
            {this.VerticalSection(mesureLength * 5.3, start * (i + 1))}
          </G>
        )
        if(i%2 == 0){
          Measures.push(
            <G height="100%" width="100%" key={keyvalue++}>
              <Path x={[mesureLength].join(' ')} y={[(i + 1) * start].join(' ')} transform={['scale(', (-1*mesureLength / 3000), spaceBetween / 650, ')'].join(' ')} style="fill:green"
                d={[MiscJson[1].data].join(' ')} />
            </G>
          )
        }

      }
    }
    return Measures;
  }

  VerticalSection(x, y) {
    return (
      <G height="100%" width="100%">
        <Line
          x1={[x].join(' ')}
          y1={[y].join(' ')}
          x2={[x].join(' ')}
          y2={[y + (4 * (SCREEN_HEIGHT / 82))].join(' ')}
          stroke="black"
          strokeWidth="1"
        />
      </G>
    )
  }

  /**
   * @deprecated Look at @renderMeasureBoxes for its replacement
   * Reason: We do not click on notes anymore you click on measures and
   * edit the measure instead of an note.
   */
  renderHitBoxes(i) {
    let mesureLength = SCREEN_WIDTH / 10;
    let start = SCREEN_HEIGHT / 8;
    let betweenNotes = SCREEN_WIDTH / 11;
    let ret = [];
    for (let j = 0; j < NotesListByMeasure[i].length; j++) {
      totalBeats += NotesListByMeasure[i][j].props.len;
      let hitBoxSize = (-1) * Math.log10(.020 * (NotesListByMeasure[i].length))
      /* Settings up vairbles */
      let xLoc = NotesListByMeasure[i][j].props._id1;

      let yLoc = Math.floor(NotesListByMeasure[i][j].props._id2 / 2);
      if (NotesListByMeasure[i][j].props._id2 % 2 != 0) {
        xLoc += 5;
      }

      yLoc += 1;
      xLoc += 1;
      // console.log("HEREREREREW" + yLoc + " : " + xLoc + " Length: " + NotesListByMeasure[i].length + " HitBox: " +  hitBoxSize);

      let pitch = NotesListByMeasure[i][j].props.pitch;

      if (NotesListByMeasure[i][j].props.note != 0) {
        ret.push(
          <Rect
            x={[((xLoc) * (SCREEN_WIDTH / 11)) + mesureLength * NoteSVG[NotesListByMeasure[i][j].props.note].HitBoxX - SCREEN_WIDTH / 70].join(' ')}
            y={[((yLoc) * (SCREEN_HEIGHT / 8)) + NoteSVG[NotesListByMeasure[i][j].props.note].HitBoxY + (NoteSVG[NotesListByMeasure[i][j].props.note].flipY * (pitch) * SCREEN_HEIGHT / 110)].join(' ')}
            width={[NoteSVG[NotesListByMeasure[i][j].props.note].flipX * (mesureLength / 1.1) * hitBoxSize].join(' ')}
            height={[NoteSVG[NotesListByMeasure[i][j].props.note].flipY * (-start / 1.6)].join(' ')}
            onPress={() => this.onPressHitBox(i, j)}
            fill="blue"
            strokeWidth="0"
            fillOpacity="0"
          />
        )
      }

    }
    return ret;
  }

  renderMeasureBoxes(i, j) {
    let spaceBetween = SCREEN_HEIGHT / 82;
    let mesureLength = SCREEN_WIDTH / 10;
    let start = SCREEN_HEIGHT / 8;
    let betweenNotes = SCREEN_WIDTH / 11;
    if (j == 0) {
      return (
        <Rect
          key={keyvalue++}
          x={[mesureLength * 1].join(' ')}
          y={[start * (i + 1) - spaceBetween].join(' ')}
          width={[mesureLength * 4.2].join(' ')}
          height={[spaceBetween * 6].join(' ')}
          onPress={() => this.onPressHitBox(0, i)}
          strokeWidth="0"
          fillOpacity="0"
        />
      )
    } else {
      return (
        <Rect
          key={keyvalue++}
          x={[mesureLength * 5.2].join(' ')}
          y={[start * (i + 1) - spaceBetween].join(' ')}
          width={[mesureLength * 4].join(' ')}
          height={[spaceBetween * 6].join(' ')}
          onPress={() => this.onPressHitBox(1, i)}
          strokeWidth="0"
          fillOpacity="0"
        />
      )
    }
  }

  onPressHitBox(x, y) {
    console.log("x: " + x + " y: " + y);
    // console.log("Before");
    // console.log(troubleCleffSplit);
    // console.log(NotesListByMeasure[(y*2) + x])
    // troubleCleffSplit[x+y].splice(0,1);
    // console.log(troubleCleffSplit[x+y]);
    // this.setState({
    //   troubleCleff: troubleCleffSplit,
    // });
    // Send to measure Screen
    if(this.state.SheetType == 0){
      this.props.navigation.navigate('ViewMeasure', {
        arr: troubleCleffSplit[2*y + x],
        full: troubleCleffSplit,
        num: (2*y + x),
        yValue: y,
        xValue: x,
        cleff: 0,
        sheetType: this.state.SheetType,
       });
    } else if(this.state.SheetType == 1){
      if(y % 2 == 0){
        // console.log("x+y: " + (x+y));
        // console.log("length: " + troubleCleffSplit.length);
        if((y+x) >= troubleCleffSplit.length){
          this.props.navigation.navigate('ViewMeasure',{
             arr: [],
             full: troubleCleffSplit,
             num: (y + x),
             yValue: y,
             xValue: x,
             cleff: 0,
             sheetType: this.state.SheetType,
           });
        } else {
          this.props.navigation.navigate('ViewMeasure', {
             arr: troubleCleffSplit[(y) + x],
             full: troubleCleffSplit,
             num: ((y) + x),
             yValue: y,
             xValue: x,
             cleff: 0,
             sheetType: this.state.SheetType,
           });
        }
      }else{
        if(((y-1)+x) >= troubleCleffSplit.length){
          this.props.navigation.navigate('ViewMeasure', {
            arr: [],
            full: baseCleffSplit,
            num: ((y-1)+x),
            yValue: y,
            xValue: x,
            cleff: 1,
            sheetType: this.state.SheetType,
          });
        }else{
          this.props.navigation.navigate('ViewMeasure', {
            arr: baseCleffSplit[((y-1)+x)],
            full: baseCleffSplit,
            num: ((y-1)+x),
            yValue: y,
            xValue: x,
            cleff: 1,
            sheetType: this.state.SheetType,
          });
        }
      }
    }
    // this.setState({ troubleCleff: troubleCleffSplit });
  }

  splitUp(troubleCleff, baseCleff, altoCleff){
    troubleCleffSplit = [];
    baseCleffSplit = [];
    let altoCleffSplit = [];

    if(this.state.SheetType == 0){
      let beats = 0;
      let tempy = [];
      let measure = 0;
      let oldbeat = 0;
      tempy.push(<NoteObjects key={keyvalue++} x={1} y={Math.ceil((measure/2) + .01)} length={0} note={0} color="black" pitch={1} />);
      for (let i = 0; i < troubleCleff.length; i++) {
        beats += troubleCleff[i].length;
        if(beats > 4){
          troubleCleffSplit.push(tempy);
          tempy = [];
          beats = troubleCleff[i].length;
          measure++;
          if(measure%2 == 0){
            tempy.push(<NoteObjects key={keyvalue++} x={1} y={Math.ceil((measure/2) + .01)} length={0} note={0} color="black" pitch={1} />);
          }
        }
        // console.log("beats: " + beats);
        let x = 2 + (beats - troubleCleff[i].length) + (4*(measure%2));
        if(troubleCleff[i].note == 8){
          console.log("FEAFEAW");
          x = (4*(measure%2)) + 3.5;
        }
        tempy.push(<NoteObjects key={keyvalue++} x={x} y={Math.ceil((measure/2) + .01)} length={troubleCleff[i].length} note={troubleCleff[i].note} color="black" pitch={troubleCleff[i].pitch} />);
        // oldbeat = troubleCleff[i].length;
      }
      if(tempy.length != 0){
        troubleCleffSplit.push(tempy);
      }
      // console.log("\n\nDone\n\n");
    }

    if(this.state.SheetType == 1){
      let beats = 0;
      let tempy = [];
      let measure = 0;
      let oldbeat = 0;
      tempy.push(<NoteObjects key={keyvalue++} x={1} y={Math.ceil((measure/2) + .01)} length={0} note={0} color="black" pitch={1} />);
      for (let i = 0; i < troubleCleff.length; i++) {
        beats += troubleCleff[i].length;
        if(beats > 4){
          troubleCleffSplit.push(tempy);
          tempy = [];
          beats = troubleCleff[i].length;
          measure++;
          if(measure%2 == 0){
            measure += 2;
            tempy.push(<NoteObjects key={keyvalue++} x={1} y={Math.ceil((measure/2) + .01)} length={0} note={0} color="black" pitch={1} />);
          }
        }
        // console.log("beats: " + beats);
        tempy.push(<NoteObjects key={keyvalue++} x={2 + (beats - troubleCleff[i].length) + (4*(measure%2))} y={Math.ceil((measure/2) + .01)} length={troubleCleff[i].length} note={troubleCleff[i].note} color="black" pitch={troubleCleff[i].pitch} />);
        // oldbeat = troubleCleff[i].length;
      }
      if(tempy.length != 0){
        troubleCleffSplit.push(tempy);
      }

      beats = 0;
      tempy = [];
      measure = 2;
      oldbeat = 0;
      tempy.push(<NoteObjects key={keyvalue++} x={1} y={Math.ceil((measure/2) + .01)} length={0} note={6} color="black" pitch={1} />);
      for (let i = 0; i < baseCleff.length; i++) {
        beats += baseCleff[i].length;
        if(beats > 4){
          baseCleffSplit.push(tempy);
          tempy = [];
          beats = baseCleff[i].length;
          measure++;
          if(measure%2 == 0){
            measure += 2;
            tempy.push(<NoteObjects key={keyvalue++} x={1} y={Math.ceil((measure/2) + .01)} length={0} note={6} color="black" pitch={1} />);
          }
        }
        // console.log("beats: " + beats);
        tempy.push(<NoteObjects key={keyvalue++} x={2 + (beats - baseCleff[i].length) + (4*(measure%2))} y={Math.ceil((measure/2) + .01)} length={baseCleff[i].length} note={baseCleff[i].note} color="black" pitch={baseCleff[i].pitch} />);
        // oldbeat = troubleCleff[i].length;
      }
      if(tempy.length != 0){
        baseCleffSplit.push(tempy);
      }
    }
  }

  initNotesListByMeasure() {
    // NotesListByMeasure = [];
    CleffLines = 0;
    let troubleCleff = [];
    let baseCleff = [];
    let altoCleff = [];
    let currentCleff = troubleCleff;
    let titles = NoteSVG[sampleJson.notes[0].note].title;
    // console.log("First Note is: " + titles);
    for (let i = 0; i < sampleJson.notes.length; i++) {
      if(NoteSVG[sampleJson.notes[i].note].title == "troubleCleff"){
        titles = "troubleCleff";
      } else if(NoteSVG[sampleJson.notes[i].note].title == "baseCleff"){
        titles = "baseCleff";
      } else if(NoteSVG[sampleJson.notes[i].note].title == "AltoCleff"){
        titles = "AltoCleff";
      } else if(titles == "troubleCleff"){
        // console.log("troubleCleff inserting " + sampleJson.notes[i].note);
        troubleCleff.push(sampleJson.notes[i]);
      } else if(titles == "baseCleff"){
        // console.log("baseCleff inserting " + sampleJson.notes[i].note);
        baseCleff.push(sampleJson.notes[i]);
      } else if(titles == "AltoCleff"){
        // console.log("AltoCleff inserting " + sampleJson.notes[i].note);
        altoCleff.push(sampleJson.notes[i]);
      }

      // if ((beatsPerMeasure + sampleJson.notes[i].length) > 4);

      // currentCleff.push(<NoteObjects key={i} _id1={xCord} _id2={NotesListByMeasure.length - 1} note={sampleJson.notes[i].note} len={sampleJson.notes[i].length} pitch={sampleJson.notes[i].pitch} color="black" />);
      // beatsPerMeasure += sampleJson.notes[i].length;
    }
    this.splitUp(troubleCleff, baseCleff, altoCleff);
  }

  displayHitBoxes() {
    let ret = [];
    let Rows = Math.max(troubleCleffSplit.length, baseCleffSplit.length, altoCleffSplit.length);
    Rows = Rows/2;
    Rows++;

    if(Rows == 0)
      Rows++;
    if(this.state.SheetType == 1){
      console.log("FEAWFEW");
      Rows *= 2;
    }
    for (var i = 0; i < Rows+1; i++) {
      ret.push(this.renderMeasureBoxes(i,0))
      ret.push(this.renderMeasureBoxes(i,1))
    }
    return ret;
  }

  renderArraysOfNotes(notes){
    console.log("Rendering");
    console.log(notes);
    let x = [];
    for (let i = 0; i < notes.length; i++) {
      for (let j = 0; j < notes[i].length; j++) {
        x.push(notes[i][j]);
      }
    }
    return x;
  }

  saveToDB(){
    const that = this;
    console.log("TROIBLECLEFFSPLITY");
    console.log(troubleCleffSplit);
    let sendIt = {};
    sendIt.clef = 0;
    sendIt.notes = [];
    for (var i = 0; i < troubleCleffSplit.length; i++) {
      for (var j = 0; j < troubleCleffSplit[i].length; j++) {
        sendIt.notes.push({"note": troubleCleffSplit[i][j].props.note, "length": troubleCleffSplit[i][j].props.length, "pitch": troubleCleffSplit[i][j].props.pitch});
      }
    }
    console.log("HERE TO STAY : ");
    console.log(sendIt);
    console.log("sheet_id : " + sheet_id);
    // fetch('http://68.183.140.180:5000/addSheetJSON', {
    //       method: 'POST',
    //       headers: {
    //           Accept: 'application/json',
    //           'Content-Type': 'application/json',
    //       },
    //       body: JSON.stringify({
    //         'file': sendIt,
    //         'sheet_id': sheet_id,
    //       }),
    //   }).then((res) => {
    //       // that.props.dispatchPlaceJSON(res._bodyText);
    //   }).catch((res) => {
    //       console.log("err", res)
    //   });

    var formData = new FormData();
    formData.append('sheet_id', sheet_id);
    formData.append('file', JSON.stringify(sendIt));
    const options = {
        method: 'POST',
        body: formData,
        formData: formData,
        headers: {'Content-Type':'multipart/form-data', 'Accept-Encoding': 'gzip, deflate', 'Cache-Control': 'no-cache'},
    }
    fetch("http://68.183.140.180:5000/addSheetJSON", options).then(result => {
        result.text().then(res => {
            console.log("camera res", res)
        }).catch(err => {
            console.log("camera err", err)
        })
    });
    this.props.navigation.state.params.onBack();
    this.props.navigation.navigate('ViewCompScreen')
  }


  render() {
    // console.log("First Render in note\n");
    keyvalue = 0;
    // screenExtendSize = 0;
    if(firstRender == 1){
      console.log("First Render in note\n");
      this.initNotesListByMeasure();
      firstRender = 0;
    }else{
      console.log("ReRendering main\n");
      newCleff = this.props.navigation.getParam('arr');
      if(this.props.navigation.getParam('cleff') == 0){
        troubleCleffSplit = newCleff;
      }else if(this.props.navigation.getParam('cleff') == 1){
        baseCleffSplit = newCleff;
      }else if(this.props.navigation.getParam('cleff') == 2){
        altoCleffSplit = newCleff;
      }
      console.log("ReRendering main\n");
    }
    // totalBeats = 0;
    backButton = require('../assets/back.png')
    let mesureLength = SCREEN_WIDTH / 10;
    let start = SCREEN_HEIGHT / 8;
    let betweenNotes = SCREEN_WIDTH / 11;
    Section = 0;

    return (
      <View style={styles.container}>
        <Header
          statusBarProps={{ barStyle: 'light-content' }}
          barStyle="light-content" // or directly
          leftComponent={
            <Button
              onPress={() => this.saveToDB()}
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
          rightComponent={
            <Button
              onPress={() => this.props.navigation.navigate('ViewExportScreen', {
                 sheet_ids: this.state.sheet_ids,
                 email: this.state.email
              })}
              icon={
                <Icon
                  name="mail"
                  size={15}
                  color="white"
                />
              }
              type="clear"
            />
          }
          centerComponent={{ text: 'Rhythm', style: { color: '#fff' } }}
          containerStyle={{
            backgroundColor: 'black',
            justifyContent: 'space-around',
          }}
        />

          <ScrollView>
            <Svg height={[screenSize + screenExtendSize].join(' ')} width="100%">
              {this.setTitle(this.props.navigation.getParam("title", "MusicSheet"))}
              {this.renderArraysOfNotes(troubleCleffSplit)}
              {this.renderArraysOfNotes(baseCleffSplit)}

              {this.lineSection()}
              {this.displayHitBoxes()}
            </Svg>

          </ScrollView>

      </View>
    )
  }
};
// <PinchZoomView maxScale={2} minScale={1}></PinchZoomView>
function mapStateToProps(state) {
  return {}
}

function mapDispatchToProps(dispatch) {
  return {}
}

//https://www.reduceimages.com/final_image.php?image=facde4b135
//30
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "white",
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

export default connect(mapStateToProps, mapDispatchToProps)(EditMusicScreen);
