/**
 * importing all the things I need to make this monster.
 * This includes but not limited to, React, react-native, react-redux,
 * react-native-easy-Grid, react-native-vector-icons/AntDesign
 * react-native-pinch-zoom-view, expo, and most importantly SVG.
 */

import React from 'react';
import { ListItem, Dimensions, TextInput, Alert, FlatList, TouchableOpacity, ScrollView, StyleSheet, View, KeyboardAvoidingView, Image, ImageBackground } from 'react-native';
// import { Header } from 'react-navigation';
import { connect } from 'react-redux';
import { Button, Header } from 'react-native-elements';
import { Col, Row, Grid } from "react-native-easy-grid";
import Icon from 'react-native-vector-icons/AntDesign'
import PinchZoomView from 'react-native-pinch-zoom-view';


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

/*
 * This is the Component that holds all the notes and
 * renders each note depending on the note num, pitch, and length
 */
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


class EditMusicScreen extends React.Component {

  constructor(props) {
    super(props);

    // sampleJson = props.navigation.getParam('file')
    // empty json file if file is null
    // if (sampleJson == null) {
    //   // sampleJson = {
    //   //   "clef": 1,
    //   //   "notes":
    //   //     [
    //   //       {
    //   //         "note": 0,
    //   //         "length": 0,
    //   //         "pitch": 1
    //   //       }
    //   //     ]
    //   // }
    //
    // }
    sampleJson = sampleJson3;

    this.state = {
      colorProp: 'black',
      alert: false,
      SheetType: 1,
      troubleCleff: troubleCleffSplit,
      baseCleff: baseCleffSplit,
    };
  }

  static navigationOptions = {
    title: 'Welcome', header: null
  };

  componentDidMount() { }

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

  pressHandler(Note) {

    if (Note.color == "red" && Note.note != 0) {
      Note.color = "black"
    } else if (Note.color == "black" && Note.note != 0) {
      Note.color = "red"
    }
    this.setState({ state: this.state });
  }

  lineSection() {
    // console.log(totalBeats);
    let Measures = [];
    let spaceBetween = SCREEN_HEIGHT / 82;
    let mesureLength = SCREEN_WIDTH / 10;
    let start = SCREEN_HEIGHT / 8;
    let betweenNotes = SCREEN_WIDTH / 11;
    let Rows = Math.ceil(totalBeats / 8);
    if(Rows == 0)
      Rows++;

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

  updateFunc(alert) {
    // console.log("GWFDigrjejgioperjgreaoyigjaw4og\n")
    // this.setState({
    //   alert: alert
    // })
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
    // console.log(NotesListByMeasure[(y*2) + x])
    // troubleCleffSplit[x+y].splice(0,1);
    // console.log(troubleCleffSplit[x+y]);
    // this.setState({
    //   troubleCleff: troubleCleffSplit,
    // });
    // Send to measure Screen
    if(this.state.SheetType == 0){
      if(((y * 2) + x) >= troubleCleffSplit.length){
        this.props.navigation.navigate('ViewMeasure', { arr: [] });
      }else{
        this.props.navigation.navigate('ViewMeasure', {
          arr: troubleCleffSplit[(y * 2) + x],
          fullT: troubleCleffSplit,
          num: ((y * 2) + x),
         });
      }
    } else if(this.state.SheetType == 1){
      if(y % 2 == 0){
        // console.log("x+y: " + (x+y));
        // console.log("length: " + troubleCleffSplit.length);
        if((y+x) >= troubleCleffSplit.length){
          this.props.navigation.navigate('ViewMeasure', { arr: [] });
        } else {
          this.props.navigation.navigate('ViewMeasure', {
             arr: troubleCleffSplit[(y) + x],
             full: troubleCleffSplit,
             num: ((y) + x),
           });
        }
      }else{
        if(((y-1)+x) >= troubleCleffSplit.length){
          this.props.navigation.navigate('ViewMeasure', { arr: [] });
        }else{
          this.props.navigation.navigate('ViewMeasure', { arr:
            baseCleffSplit[(y-1) + x],
            full: baseCleffSplit,
            num: ((y-1) + x),
           });
        }
      }
    }

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
        tempy.push(<NoteObjects key={keyvalue++} x={2 + (beats - troubleCleff[i].length) + (4*(measure%2))} y={Math.ceil((measure/2) + .01)} length={troubleCleff[i].length} note={troubleCleff[i].note} color="black" pitch={troubleCleff[i].pitch} />);
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
    let Rows = Math.ceil(totalBeats / 8);
    if(Rows == 0)
      Rows++;
    for (var i = 0; i < Rows+1; i++) {
      ret.push(this.renderMeasureBoxes(i,0))
      ret.push(this.renderMeasureBoxes(i,1))
    }
    return ret;
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
      console.log(troubleCleffSplit);
      console.log("ReRendering main\n");
    }

    // console.log(NotesListByMeasure.props.note);
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
              onPress={() => this.props.navigation.navigate('ViewCompScreen')}
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
            backgroundColor: 'black',
            justifyContent: 'space-around',
          }}
        />

          <ScrollView>
            <Svg height={[screenSize + screenExtendSize].join(' ')} width="100%">
              {this.setTitle(this.props.navigation.getParam("title", "MusicSheet"))}
              {troubleCleffSplit}
              {baseCleffSplit}

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
