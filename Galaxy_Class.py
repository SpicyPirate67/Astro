
import json
import matplotlib.pyplot as plt
import numpy as np

class Galaxy:
    def __init__(self, Convert_Images, analyze_classification, colour_plots, json_path, img_path):
        self.Convert_Images = Convert_Images
        self.analyze_classification = analyze_classification
        self.colour_plots = colour_plots
        self.img_path = img_path
        self.json_path = json_path
    
    #Set the booleans
    def set_convert_images(self, state):
        self.Convert_Images = state

    def set_analyze_classification(self, state):
        self.analyze_classification = state

    def set_colour_plots(self, state):
        self.colour_plots = state
    
    #Set and Get the paths for JSON and img
    def set_json_path(self, json_path):
        self.json_path = json_path
        
    def get_json_path(self):
        return self.json_path
    
    def set_img_path(self, img_path):
        self.img_path = img_path
        
    def get_img_path(self):
        return self.img_path

    #iterates through json and does selected operations
    def func(self): 

        with open(self.json_path) as json_file:
            self.data = json.load(json_file)

        self.spirals = []
        self.ellipticals = []
        self.uncertains = []

        #Numpy arrays for scatter plot
        self.x_data_spiral = np.array([])
        self.y_data_spiral = np.array([])
        self.x_data_elliptical = np.array([])
        self.y_data_elliptical = np.array([])
        self.x_data_uncertain = np.array([])
        self.y_data_uncertain = np.array([])

        self.seperator_x = np.array([])
        
        for i in self.data[0]:
            self.num = 1
            for j in self.data[0][i]:
                if type(j) == dict:
                    specObjID = j["specObjID"]
                    spiral = j["spiral"]
                    elliptical = j["elliptical"]
                    uncertain = j["uncertain"]
                    
                    if self.Convert_Images:
                        name = f"{self.img_path}{self.num}({specObjID}).jpg"
                        self.convertImage(j["img"], name)
                    
                    if self.analyze_classification:
                        if spiral:
                            self.spirals.append(self.num)
                        elif elliptical:
                            self.ellipticals.append(self.num)
                        elif uncertain:
                            self.uncertains.append(self.num)

                    if self.colour_plots:
                        #Convert to Magnitude
                        self.spect_u = self.maggie_convertion(j["spectroFlux_u"])
                        self.spect_g = self.maggie_convertion(j["spectroFlux_g"])
                        self.spect_r = self.maggie_convertion(j["spectroFlux_r"])

                        self.u_g = self.spect_u - self.spect_g
                        self.g_r = self.spect_g - self.spect_r

                        if spiral:
                            self.x_data_spiral = np.append(self.x_data_spiral, [self.u_g])
                            self.y_data_spiral = np.append(self.y_data_spiral, [self.g_r])
                        elif elliptical:
                            self.x_data_elliptical = np.append(self.x_data_elliptical, [self.u_g])
                            self.y_data_elliptical = np.append(self.y_data_elliptical, [self.g_r])
                        elif uncertain:
                            self.x_data_uncertain = np.append(self.x_data_uncertain, [self.u_g])
                            self.y_data_uncertain = np.append(self.y_data_uncertain, [self.g_r])
                        
                        self.seperator_x = np.append(self.seperator_x, [self.spect_u])

                    self.num += 1

        if self.analyze_classification:
            print(self.spirals)
            print(self.ellipticals)
            print(self.uncertains)

            self.total_galaxies = len(self.spirals) + len(self.ellipticals) + len(self.uncertains)
            self.ratio_spiral = len(self.spirals) / self.total_galaxies
            self.ratio_ellipticals = len(self.ellipticals) / self.total_galaxies
            self.ratio_uncertain = len(self.uncertains) / self.total_galaxies

            print(f"Spirals: {self.ratio_spiral}, Ellipticals: {self.ratio_ellipticals}, Uncertains: {self.ratio_uncertain}")

    def maggie_convertion(self, data):
        self.flux = data*10**9
        self.mag = 22.5 - (2.5*np.log10(self.flux))
        return self.mag

    def drawPlot(self):
        if not self.colour_plots:
            return

        fig, ax = plt.subplots()
        ax.scatter(self.x_data_spiral, self.y_data_spiral, marker="*", label="Spirals")
        ax.scatter(self.x_data_elliptical, self.y_data_elliptical, marker="X", label="Ellipticals")
        ax.scatter(self.x_data_uncertain, self.y_data_uncertain, marker="s", label="Uncertain")

        self.line_x = np.linspace(0.5,2,100)
        self.line_y = [-i+2.22 for i in self.line_x]

        ax.plot(self.line_x, self.line_y, label="U-R=2.22")
        plt.title("Colour Colour plot")
        plt.xlabel("G-R")
        plt.ylabel("U-G")
        plt.legend(loc='upper left')

        plt.show()

    #Converts varbin to an image and saves it
    def convertImage(self, image_data, name):
        
        self.integers = []
        image_data = image_data[2:]
        
        while image_data:
            value = int(image_data[:2], 16)
            self.integers.append(value)
            image_data = image_data[2:]
        
        self.data = bytearray(self.integers)    
            
        with open(name, 'xb') as fh:
            print(fh.write(self.data))
