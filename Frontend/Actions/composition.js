import { ADD_COMPOSITION } from './types';

export const addComposition = compositionName => {
  return {
    type: ADD_COMPOSITION,
    payload: compositionName
  }
}