from omrdatasettools.image_generators.HomusImageGenerator import HomusImageGenerator

# run this to convert the text for strokes into image format
# done with stafflie vertical offset as none because don't want staff lines while training

HomusImageGenerator.create_images(raw_data_directory="./SymbolsDataset",
                                  destination_directory="./SymbolsDatasetParsed",
                                  stroke_thicknesses=[2],
                                  canvas_width=50,
                                  canvas_height=70,
                                  staff_line_spacing=14,
                                  staff_line_vertical_offsets=None)