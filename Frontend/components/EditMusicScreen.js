import React from 'react';
import { ListItem, Dimensions,TextInput, Alert, FlatList, TouchableOpacity, ScrollView, StyleSheet, View, KeyboardAvoidingView, Image, ImageBackground } from 'react-native';
// import { Header } from 'react-navigation';
import { connect } from 'react-redux';
import { Button, Header } from 'react-native-elements';
import { Col, Row, Grid } from "react-native-easy-grid";
import Icon from 'react-native-vector-icons/AntDesign'
import PinchZoomView from 'react-native-pinch-zoom-view';
// import Svg,{
//     Circle
// } from 'react-native-svg';


import { Svg } from 'expo';
const { Circle, Rect, Path, Line, Text, G, Defs, Use } = Svg;

// https://oblador.github.io/react-native-vector-icons/
var sampleJson = require('./SampleMusicSheet.json');
var NoteSVG = require('./NotesData.json');
var MiscJson = require('./EditMisc.json');
var NotesList = [];
// var ran1 = [0,5,10,15,20,25,30,35,40,45,50,55]

// var styles = require('../style');
const SCREEN_WIDTH = Dimensions.get('window').width
const SCREEN_HEIGHT = Dimensions.get('window').height
var colorr = "#00ffff";
var idCounter = 0;
var Section;
var totalBeats;
var screenSize = SCREEN_HEIGHT;

class NoteObjects {
  constructor(note, length, pitch){
    this._id = idCounter++;
    this.note = note;
    this.length = length;
    this.pitch = pitch;
    this.color = "black";
  }
}


class EditMusicScreen extends React.Component {

  constructor(props) {
      super(props);
      NotesList = [];

      for (let i = 0; i < sampleJson.notes.length; i++) {
        NotesList.push(new NoteObjects(sampleJson.notes[i].note, sampleJson.notes[i].length, sampleJson.notes[i].pitch));
      }
      // console.log(NotesList);
      this.state = {
        NotesL: NotesList,
        colorProp: 'black',
      };


  }
  static navigationOptions = {
      title: 'Welcome', header: null
  };

  componentDidMount() {}

  // lapsList() {
  //   let s;
  //   return NotesList.map((item) => {
  //     return <ListItem image={item.note}/>
  //   })
  // }
  setTitle(title){
    let start = SCREEN_HEIGHT/8;
    return (
      <Svg height="100%" width="100%">
        <Text
            stroke="black"
            fontSize="20"
            x={[SCREEN_WIDTH/2].join(' ')}
            y={[start/2].join(' ')}
            textAnchor="middle"
        >{title}</Text>
      </Svg>
    )
  }

  placeVerticalLines(line){
    let mesureLength = SCREEN_WIDTH/10;
    let start = SCREEN_HEIGHT/8;
    start *= line
    return (
      <Svg height="100%" width="100%">
        {this.VerticalSection(mesureLength, start)}
        {this.VerticalSection(mesureLength*5.25, start)}
        {this.VerticalSection(mesureLength*9.05, start)}
      </Svg>
    )
  }

  pressHandler(Note){

    if (Note.color == "red" && Note.note != 0){
      Note.color = "black"
    }else if(Note.color == "black" && Note.note != 0){
      Note.color = "red"
    }
    this.setState({ state: this.state });
  }

  lineSection(){
    let amountOfMeasure = [];
    let spaceBetween = SCREEN_HEIGHT/82;
    let mesureLength = SCREEN_WIDTH/10;
    let start = SCREEN_HEIGHT/8;
    let betweenNotes = SCREEN_WIDTH/11;
    Section++;
    let x = 1;
    if(Section%2 == 0)
      x = 4.8;
    let y = Math.floor(Section/2);
    if(Section == 1){
      y = 0;
    }
    // console.log((((parseInt(Math.ceil((NotesList.length)/4.5/2))+1)*start + (5*SCREEN_HEIGHT/110)) + ":" + screenSize)
    if(((parseInt(Math.ceil((NotesList.length)/4.5/2))+1)*start + (5*SCREEN_HEIGHT/110)) > screenSize){
      screenSize += 100;
    }
    for (let i = 0; i < Math.ceil((NotesList.length)/4.5); i++) {


      amountOfMeasure.push(
        <Svg height="100%" width="100%">
          <Path x={[x*mesureLength].join(' ')} y={[((parseInt(i/2))+1)*start].join(' ')} transform={['scale(', .8, .4, ')'].join(' ')}  style="fill:green"
          d={[MiscJson[0].data].join(' ')}/>
          {this.placeVerticalLines(((parseInt(i/2))+1))}
        </Svg>
      )
    }
    return amountOfMeasure
  }

  VerticalSection(x, y){
    return (
      <Svg height="100%" width="100%">
        <Line
            x1={[x].join(' ')}
            y1={[y].join(' ')}
            x2={[x].join(' ')}
            y2={[y+(4*(SCREEN_HEIGHT/82))].join(' ')}
            stroke="black"
            strokeWidth="1"
        />
      </Svg>
    )
  }
// 0 1  2  3  4  5  6  7  8
// 9 10 11 12 13 14 15 16 17
  //https://www.online-convert.com/result/12158467-08e6-47c0-9ecc-d809e5f78bbc
  // note, x, y length, pitch
  Notes(Note){
    // console.log(screenSize);
    let mesureLength = SCREEN_WIDTH/10;
    let start = SCREEN_HEIGHT/8;
    let betweenNotes = SCREEN_WIDTH/11;
    let x = (Note._id%9)
    let y = Math.ceil(Note._id/9);
    if(Note._id == 0){
      y = 1;
    }else if(Note._id%9 == 0){
      y++;
    }
    let pitch = Note.pitch;
    if(pitch == 0)
     pitch++;
    // if(x == 0){
    //   x = 1;
    // }
    x++;
    // console.log("X: " + x + " Y: " + y);
    // console.log(Note)
    return (
        <G x="0" stroke="black" stroke-width="0" y="0" fill={[Note.color].join(' ')}>
          <Path x={[((x)*(SCREEN_WIDTH/11))+NoteSVG[Note.note].adjustX].join(' ')} y={([((y)*(SCREEN_HEIGHT/8))+ (Note.pitch*SCREEN_HEIGHT/164) + NoteSVG[Note.note].adjustY].join(' '))} transform={['scale(', NoteSVG[Note.note].scale1, NoteSVG[Note.note].scale2, ')'].join(' ')} d={[NoteSVG[Note.note].data].join(' ')}/>
          <Rect
            x={[((x)*(SCREEN_WIDTH/11)) + mesureLength*NoteSVG[Note.note].HitBoxX].join(' ')}
            y={[((y)*(SCREEN_HEIGHT/8)) + NoteSVG[Note.note].HitBoxY + (NoteSVG[Note.note].flipY*(pitch)*SCREEN_HEIGHT/110)].join(' ')}
            width={[NoteSVG[Note.note].flipX * (mesureLength/1.1)].join(' ')}
            height={[NoteSVG[Note.note].flipY * (-start/1.6)].join(' ')}
            fill="none"
            strokeWidth="1"
            onPress={this.pressHandler.bind(this, Note)}
          />
        </G>
    )
  }

  setNotes(Notes){
    let NotesL = [];
    for (let i = 0; i < NotesList.length; i++) {
      NotesL.push(this.Notes(Notes[i]))
    }
      return NotesL;
  }

  render(){
    totalBeats = 0;
    backButton = require('../assets/back.png')
    let mesureLength = SCREEN_WIDTH/10;
    let start = SCREEN_HEIGHT/8;
    let betweenNotes = SCREEN_WIDTH/11;
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
          <Svg height={[screenSize].join(' ')}  width="100%">
            {this.setTitle("Steven is the Best")}
            {this.lineSection()}
            {this.lineSection()}
            {this.setNotes(NotesList)}
          </Svg>
        </ScrollView>
      </View>
    )
  }
};

// <Image
//   style={styles.Notes}
//   source={require('../assets/mesure.png')}
// />
  function mapStateToProps(state) {}

  function mapDispatchToProps(dispatch) {}

//https://www.reduceimages.com/final_image.php?image=facde4b135
//30
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

  export default connect(mapStateToProps, mapDispatchToProps)(EditMusicScreen);


  // <G x={[mesureLength].join(' ')} y={[start].join(' ')} onPressIn={this.pressHandler.bind(this,1, 1)}><Path fill="white" d={["M0 0 V", start/2, " H", 4.2*mesureLength," V0 Z"].join(' ')} /></G>
  // <G x={[mesureLength + 4.2*mesureLength].join(' ')} y={[start].join(' ')} onPressIn={this.pressHandler.bind(this,1, 2)}><Path fill="white" d={["M0 0 V", start/2, " H", 4.2*mesureLength," V0 Z"].join(' ')} /></G>
  // <G x={[mesureLength].join(' ')} y={[2*start].join(' ')} onPressIn={this.pressHandler.bind(this,2, 1)}><Path fill="white" d={["M0 0 V", start/2, " H", 4.2*mesureLength," V0 Z"].join(' ')} /></G>
  // <G x={[mesureLength + 4.2*mesureLength].join(' ')} y={[2*start].join(' ')} onPressIn={this.pressHandler.bind(this,2, 2)}><Path fill="white" d={["M0 0 V", start/2, " H", 4.2*mesureLength," V0 Z"].join(' ')} /></G>
  // <G x={[mesureLength].join(' ')} y={[3*start].join(' ')} onPressIn={this.pressHandler.bind(this,3, 1)}><Path fill="white" d={["M0 0 V", start/2, " H", 4.2*mesureLength," V0 Z"].join(' ')} /></G>
  // <G x={[mesureLength + 4.2*mesureLength].join(' ')} y={[3*start].join(' ')} onPressIn={this.pressHandler.bind(this,3, 2)}><Path fill="white" d={["M0 0 V", start/2, " H", 4.2*mesureLength," V0 Z"].join(' ')} /></G>
  // <G x={[mesureLength].join(' ')} y={[4*start].join(' ')} onPressIn={this.pressHandler.bind(this,4, 1)}><Path fill="white" d={["M0 0 V", start/2, " H", 4.2*mesureLength," V0 Z"].join(' ')} /></G>
  // <G x={[mesureLength + 4.2*mesureLength].join(' ')} y={[4*start].join(' ')} onPressIn={this.pressHandler.bind(this,4, 2)}><Path fill="white" d={["M0 0 V", start/2, " H", 4.2*mesureLength," V0 Z"].join(' ')} /></G>
  // <G x={[mesureLength].join(' ')} y={[5*start].join(' ')} onPressIn={this.pressHandler.bind(this,5, 1)}><Path fill="white" d={["M0 0 V", start/2, " H", 4.2*mesureLength," V0 Z"].join(' ')} /></G>
  // <G x={[mesureLength + 4.2*mesureLength].join(' ')} y={[5*start].join(' ')} onPressIn={this.pressHandler.bind(this,5, 2)}><Path fill="white" d={["M0 0 V", start/2, " H", 4.2*mesureLength," V0 Z"].join(' ')} /></G>
  // <G x={[mesureLength].join(' ')} y={[6*start].join(' ')} onPressIn={this.pressHandler.bind(this,6, 1)}><Path fill="white" d={["M0 0 V", start/2, " H", 4.2*mesureLength," V0 Z"].join(' ')} /></G>
  // <G x={[mesureLength + 4.2*mesureLength].join(' ')} y={[6*start].join(' ')} onPressIn={this.pressHandler.bind(this,6, 2)}><Path fill="white" d={["M0 0 V", start/2, " H", 4.2*mesureLength," V0 Z"].join(' ')} /></G>
  // <G x={[mesureLength].join(' ')} y={[7*start].join(' ')} onPressIn={this.pressHandler.bind(this,7, 1)}><Path fill="white" d={["M0 0 V", start/2, " H", 4.2*mesureLength," V0 Z"].join(' ')} /></G>
  // <G x={[mesureLength + 4.2*mesureLength].join(' ')} y={[7*start].join(' ')} onPressIn={this.pressHandler.bind(this,7, 2)}><Path fill="white" d={["M0 0 V", start/2, " H", 4.2*mesureLength," V0 Z"].join(' ')} /></G>
