import sys, random, enum, ast, time, threading, os, math, contextlib
from rpy2 import robjects
    
def R_to_Py_plot_priority(people, smoke, location, image_name):
    """ function to run the R code required for creating the SHAP plot in the situation extinguish or evacuate first """
    r_script = (f'''
                # preprocess data
                data <- read_excel("data/moral_sensitivity_survey_data.xlsx")
                data$situation <- as.factor(data$situation)
                data$location <- as.factor(data$location)
                data$smoke <- as.factor(data$smoke)
                data_subset <- subset(data, data$situation == "3" | data$situation == "6")
                data_subset <- data_subset[data_subset$smoke != "pushing out",]
                data_subset$people <- as.numeric(data_subset$people)
                # fit linear regression model based on the subset that ensured all assumptions are met
                fit <- lm(sensitivity ~ people + smoke + location, data = data_subset[-c(293, 205, 199, 162, 144, 122, 94, 76, 74, 18),])
                # create prediction dataset
                pred_data <- subset(data_subset[-c(293, 205, 199, 162, 144, 122, 94, 76, 74, 18),], select = c("people", "smoke", "location", "sensitivity"))
                pred_data$smoke <- factor(pred_data$smoke, levels = c("fast", "normal", "slow"))
                # fit the explainer model using SHAP
                explainer <- shapr(pred_data, fit)
                # determine the baseline moral sensitivity
                baseline_sensitivity <- mean(pred_data$sensitivity)
                # create a new dataframe with predictions for unseen data
                new_data <- data.frame(people = c({people}), smoke = c("{smoke}"), location = c("{location}"))
                new_data$smoke <- factor(new_data$smoke, levels = c("fast", "normal", "slow"))
                new_data$location <- factor(new_data$location, levels = c("known", "unknown"))
                # extract the explanation for the prediction
                explanation <- shapr::explain(new_data, approach = "ctree", explainer = explainer, prediction_zero = baseline_sensitivity)
                # extract the explanation plot for the prediction
                explanation_plot <- plot(explanation, digits = 1, plot_phi0 = TRUE) 
                # extract the data underlying the plot
                data_plot <- explanation_plot[["data"]]
                data_plot$phi <- round(data_plot$phi, 1)
                # extract the prediction value from the data and round it 
                new_pred <- round(sum(data_plot$phi), 1)
                # rename some variables for prettier plots and replace text with symbols
                min <- 'min.'
                loc <- NA
                if ("{location}" == 'known') {{loc <- 'found'}}
                if ("{location}" == 'unknown') {{loc <- '?'}}
                labels <- c(none = "<br> baseline <br> moral <br> sensitivity", 
                smoke = paste("<img src='images/smoke_speed_black.png' width='53' /><br>\n", new_data$smoke), 
                location = paste("<img src='images/location_fire_black.png' width='35' /><br>\n", loc), 
                people = paste("<img src='images/victims.png' width='19' /><br>\n", new_data$people))
                # reorder the plot so it starts with the baseline moral sensitivity and then descending feature importance
                index <- 1
                original_rank <- data_plot$rank[index]
                data_plot$rank[data_plot$rank < original_rank] <- data_plot$rank[data_plot$rank < original_rank] + 1
                data_plot$rank[index] <- 1
                order_indices <- order(data_plot$rank)
                data_plot <- data_plot[order_indices, ]
                data_plot$variable <- factor(data_plot$variable, levels = unique(data_plot$variable))
                # create the final plot
                final_plot <- ggplot(data_plot, aes(x = variable, y = phi, fill = ifelse(data_plot$variable == "none", "#3E6F9F", ifelse(data_plot$phi >= 0, "#dc4c5d", "#117733")))) + 
                geom_bar(stat = "identity") + 
                geom_text(aes(label = ifelse(data_plot$variable=="none", phi, ifelse(data_plot$phi>=0, paste("+", phi, sep=""), paste("-", abs(phi)))),
                y = ifelse(phi >= 0, phi + 0.1, phi - 0.1)), family = "sans-serif", color = "black", size = 4, vjust = ifelse(data_plot$phi >= 0, 0.4, 0.6)) + 
                scale_x_discrete(name = NULL, labels = labels) +
                theme(axis.text.x = ggtext::element_markdown()) + 
                theme(text = element_text(size = 5, family = "sans-serif"), plot.title = element_text(hjust = 0.5, size = 12, color = "black", face = "bold", margin = margin(b = 5)),
                plot.caption = element_text(size = 12, margin = margin(t = 25), color = "black"), panel.background = element_blank(), axis.text = element_text(size = 12, color = "black"),
                axis.text.y = element_text(color = "black", margin = margin(t = 5)), axis.line = element_line(color = "black"), axis.title = element_text(size = 12),
                axis.title.y = element_text(color = "black", margin = margin(r = 10), hjust = 0.5), axis.title.x = element_text(color = "black", margin = margin(t = 5), hjust = 0.5),
                panel.grid.major = element_line(color = "#DAE1E7"), panel.grid.major.x = element_blank()) +
                theme(legend.background = element_rect(fill = "white", color = "white"), legend.key = element_rect(fill = "white", color = "white"), legend.text = element_text(size = 12),
                legend.position = "none", legend.title = element_text(size = 12, face = "plain")) +
                labs(y = "Contribution to predicted sensitivity", fill = "") + 
                scale_fill_manual(values = c("#3E6F9F" = "#3E6F9F", "#117733" = "#117733", "#dc4c5d" = "#dc4c5d"), labels = c("#3E6F9F" = "Baseline", "#117733" = "Increase", "#dc4c5d" = "Decrease")) + 
                geom_hline(yintercept = 0, color = "black") + 
                theme(axis.text = element_text(color = "black"), axis.ticks = element_line(color = "black"))
                # adjust image size and save it
                dpi_web <- 300
                width_pixels <- 1500
                height_pixels <- 1500
                width_inches_web <- width_pixels / dpi_web
                height_inches_web <- height_pixels / dpi_web
                ggsave(filename = "{image_name}", plot = final_plot, width = width_inches_web, height = height_inches_web, dpi = dpi_web)
                ''')
    # execute the R script
    with open(os.devnull, 'w') as nullfile:
        with contextlib.redirect_stdout(nullfile), contextlib.redirect_stderr(nullfile):
            robjects.r(r_script)
    # extract and return the predicted moral sensitivity
    sensitivity = robjects.r['new_pred'][0]
    return sensitivity

def R_to_Py_plot_tactic(people, location, resistance, image_name):
    """ function to rund the R code required for creating the SHAP plot in the situation continue or switch deployment tactic """
    r_script = (f'''
                # preprocess data
                data <- read_excel("data/moral_sensitivity_survey_data.xlsx")
                data$situation <- as.factor(data$situation)
                data$location <- as.factor(data$location)
                data_subset <- subset(data, data$situation=="5" | data$situation=="7")
                data_subset$people[data_subset$people == "0"] <- "none"
                data_subset$people[data_subset$people == "1"] <- "one"
                data_subset$people[data_subset$people == "10" | data_subset$people == "11" | data_subset$people == "2" | data_subset$people == "3" | data_subset$people == "4" | data_subset$people == "5"] <- "multiple"
                data_subset <- data_subset[data_subset$people != "clear",]
                data_subset$people <- factor(data_subset$people, levels = c("none","unclear","one","multiple"))
                # fit linear regression model based on the subset that ensured all assumptions are met
                fit <- lm(sensitivity ~ people + resistance + location, data = data_subset[-c(266, 244, 186, 178, 126, 111, 97, 44, 19),])
                # create prediction dataset
                pred_data <- subset(data_subset[-c(266, 244, 186, 178, 126, 111, 97, 44, 19),], select = c("people", "resistance", "location", "sensitivity"))
                # fit the explainet model used SHAP
                explainer <- shapr(pred_data, fit)
                # determine the baseline moral sensitivity
                baseline_sensitivity <- mean(pred_data$sensitivity)
                # create a new dataframe with predictions for unseen data
                new_data <- data.frame(people = c("{people}"), resistance = c({resistance}), location = c("{location}"))
                new_data$people <- factor(new_data$people, levels = c("none", "unclear", "one", "multiple"))
                new_data$location <- factor(new_data$location, levels = c("known", "unknown"))
                # extract the explanation for the prediction
                explanation <- shapr::explain(new_data, approach = "ctree", explainer = explainer, prediction_zero = baseline_sensitivity)
                # extract the explanation plot for the prediction
                explanation_plot <- plot(explanation, digits = 1, plot_phi0 = TRUE) 
                # extract the data underlying the plot
                data_plot <- explanation_plot[["data"]]
                data_plot$phi <- round(data_plot$phi, 1)
                # extract the prediction valye from the data and round it
                new_pred <- round(sum(data_plot$phi), 1)
                # rename some variables for prettier plots and replace text with symbols
                min <- 'min.'
                loc <- NA
                if ("{location}" == 'known') {{ loc <- 'found'}}
                if ("{location}" == 'unknown') {{ loc <- '?'}}
                labels <- c(none = "<br> baseline <br> moral <br> sensitivity", 
                resistance = paste("<img src='images/fire_resistance_black.png' width='38' /><br>\n", new_data$resistance, min), 
                location = paste("<img src='images/location_fire_black.png' width='35' /><br>\n", loc), 
                people = paste("<img src='images/victims.png' width='19' /><br>\n", new_data$people))
                # reorder the plot so it starts with the baseline moral sensitivity and then descending feature importance
                index <- 1
                original_rank <- data_plot$rank[index]
                data_plot$rank[data_plot$rank < original_rank] <- data_plot$rank[data_plot$rank < original_rank] + 1
                data_plot$rank[index] <- 1
                order_indices <- order(data_plot$rank)
                data_plot <- data_plot[order_indices, ]
                data_plot$variable <- factor(data_plot$variable, levels = unique(data_plot$variable))
                # create the final plot
                final_plot <- ggplot(data_plot, aes(x = variable, y = phi, fill = ifelse(data_plot$variable == "none", "#3E6F9F", ifelse(data_plot$phi >= 0, "#dc4c5d", "#117733")))) +
                geom_bar(stat = "identity") +
                geom_text(aes(label = ifelse(data_plot$variable=="none", phi, ifelse(data_plot$phi>=0, paste("+", phi, sep=""), paste("-", abs(phi)))),
                y = ifelse(phi >= 0, phi + 0.1, phi - 0.1)), family = "sans-serif", color = "black", size = 4, 
                vjust = ifelse(data_plot$phi >= 0, 0.4, 0.6)) +
                scale_x_discrete(name = NULL, labels = labels) +
                theme(axis.text.x = ggtext::element_markdown()) +
                theme(text = element_text(size = 5, family = "sans-serif"), plot.title = element_text(hjust = 0.5, size = 12, color = "black", face = "bold", margin = margin(b = 5)),
                plot.caption = element_text(size = 12, margin = margin(t = 25), color = "black"), panel.background = element_blank(),
                axis.text = element_text(size = 12, color = "black"), axis.text.y = element_text(color = "black", margin = margin(t = 5)), axis.line = element_line(color = "black"),
                axis.title = element_text(size = 12), axis.title.y = element_text(color = "black", margin = margin(r = 10), hjust = 0.5), axis.title.x = element_text(color = "black", margin = margin(t = 5), hjust = 0.5),
                panel.grid.major = element_line(color = "#DAE1E7"), panel.grid.major.x = element_blank()) +
                theme(legend.background = element_rect(fill = "white", color = "white"), legend.key = element_rect(fill = "white", color = "white"), legend.text = element_text(size = 12),
                legend.position = "none", legend.title = element_text(size = 12, face = "plain")) +
                labs(y = "Contribution to predicted sensitivity", fill = "") + 
                scale_fill_manual(values = c("#3E6F9F" = "#3E6F9F", "#117733" = "#117733", "#dc4c5d" = "#dc4c5d"), labels = c("#3E6F9F" = "Baseline", "#117733" = "Increase", "#dc4c5d" = "Decrease")) + 
                geom_hline(yintercept = 0, color = "black") + theme(axis.text = element_text(color = "black"), axis.ticks = element_line(color = "black"))
                # rescale image and save it
                dpi_web <- 300
                width_pixels <- 1500
                height_pixels <- 1500
                width_inches_web <- width_pixels / dpi_web
                height_inches_web <- height_pixels / dpi_web
                ggsave(filename = "{image_name}", plot=final_plot, width = width_inches_web, height = height_inches_web, dpi = dpi_web)
                ''')
    # execute R script
    with open(os.devnull, 'w') as nullfile:
        with contextlib.redirect_stdout(nullfile), contextlib.redirect_stderr(nullfile):
            robjects.r(r_script)
    # extract predicted moral sensitivity
    sensitivity = robjects.r['new_pred'][0]
    return sensitivity

def R_to_Py_plot_locate(people, resistance, temperature, image_name):
    """ function to execute R script for running SHAP and creating the feature importance plot for the situation send in firefighters to locate fire source """
    r_script = (f'''
                # data preprocessing
                data <- read_excel("data/moral_sensitivity_survey_data.xlsx")
                data$situation <- as.factor(data$situation)
                data$temperature <- as.factor(data$temperature)
                data_subset <- subset(data, data$situation == "2" | data$situation == "4")
                data_subset$people[data_subset$people == "0"] <- "none"
                data_subset$people[data_subset$people == "1"] <- "one"
                data_subset$people[data_subset$people == "10" | data_subset$people == "11" | data_subset$people == "2" | data_subset$people == "3" | data_subset$people == "4" | data_subset$people == "40" | data_subset$people == "5"] <- "multiple"
                data_subset <- data_subset[data_subset$people != "clear",]
                data_subset$people <- factor(data_subset$people, levels = c("none", "unclear", "one", "multiple"))
                data_subset <- data_subset %>% drop_na(duration)
                # fit regression model using the subset that ensures all assumptions are met
                fit <- lm(sensitivity ~ people + resistance + temperature, data = data_subset[-c(220, 195, 158, 126, 121, 76),])
                # create prediction data set
                pred_data <- subset(data_subset[-c(220, 195, 158, 126, 121, 76),], select = c("people", "resistance", "temperature", "sensitivity"))
                # fit the explainer using SHAP
                explainer <- shapr(pred_data, fit)
                # determine the baseline moral sensitivity
                baseline_sensitivity <- mean(pred_data$sensitivity)
                # create a new dataframe for predictions on unseen data
                new_data <- data.frame(resistance = c({resistance}), temperature = c("{temperature}"), people = c("{people}"))
                new_data$temperature <- factor(new_data$temperature, levels = c("close", "higher", "lower"))
                new_data$people <- factor(new_data$people, levels = c("none", "unclear", "one", "multiple"))
                # generate a prediction using SHAP
                explanation <- shapr::explain(new_data, approach = "ctree", explainer = explainer, prediction_zero = baseline_sensitivity)
                explanation_plot <- plot(explanation, digits = 1, plot_phi0 = TRUE) 
                # extract the data underlying the plot
                data_plot <- explanation_plot[["data"]]
                data_plot$phi <- round(data_plot$phi, 1)
                # extract and round the predicted value
                new_pred <- round(sum(data_plot$phi), 1)
                # rename some variables for prettier plotting and replace text with symbols
                min <- 'min.'
                temp <- NA
                if ("{temperature}" == 'close') {{ temp <- '<≈ thresh.' }}
                if ("{temperature}" == 'lower') {{ temp <- '&lt; thresh.' }}
                if ("{temperature}" == 'higher') {{ temp <- '&gt; thresh.' }}
                labels <- c(none = "<br> baseline <br> moral <br> sensitivity", 
                resistance = paste("<img src='images/fire_resistance_black.png' width='38' /><br>\n", new_data$resistance, min), 
                temperature = paste("<img src='images/celsius_transparent.png' width='43' /><br>\n", temp), 
                people = paste("<img src='images/victims.png' width='19' /><br>\n", new_data$people))
                # reorder variables so that plot starts with baseline sensitivity and then descending feature importance
                index <- 1
                original_rank <- data_plot$rank[index]
                data_plot$rank[data_plot$rank < original_rank] <- data_plot$rank[data_plot$rank < original_rank] + 1
                data_plot$rank[index] <- 1
                order_indices <- order(data_plot$rank)
                data_plot <- data_plot[order_indices, ]
                data_plot$variable <- factor(data_plot$variable, levels = unique(data_plot$variable))
                # create final plot
                final_plot <- ggplot(data_plot, aes(x = variable, y = phi, fill = ifelse(data_plot$variable == "none", "#3E6F9F", ifelse(data_plot$phi >= 0, "#dc4c5d", "#117733")))) +
                geom_bar(stat = "identity") +
                geom_text(aes(label = ifelse(data_plot$variable=="none", phi, ifelse(data_plot$phi>=0, paste("+", phi, sep=""), paste("-", abs(phi)))),
                y = ifelse(phi >= 0, phi + 0.1, phi - 0.1)), family = "sans-serif", color = "black", size = 4, vjust = ifelse(data_plot$phi >= 0, 0.4, 0.6)) +
                scale_x_discrete(name = NULL, labels = labels) +
                theme(axis.text.x = ggtext::element_markdown()) +
                theme(text = element_text(size = 5, family = "sans-serif"),
                plot.title = element_text(hjust = 0.5, size = 12, color = "black", face = "bold", margin = margin(b = 5)), plot.caption = element_text(size = 12, margin = margin(t = 25), color = "black"),
                panel.background = element_blank(), axis.text = element_text(size = 12, color = "black"), axis.text.y = element_text(color = "black", margin = margin(t = 5)), axis.line = element_line(color = "black"),
                axis.title = element_text(size = 12), axis.title.y = element_text(color = "black", margin = margin(r = 10), hjust = 0.5), axis.title.x = element_text(color = "black", margin = margin(t = 5), hjust = 0.5),
                panel.grid.major = element_line(color = "#DAE1E7"), panel.grid.major.x = element_blank()) +
                theme(legend.background = element_rect(fill = "white", color = "white"), legend.key = element_rect(fill = "white", color = "white"), legend.text = element_text(size = 12), legend.position = "none", legend.title = element_text(size = 12, face = "plain")) +
                labs(y = "Contribution to predicted sensitivity", fill = "") + 
                scale_fill_manual(values = c("#3E6F9F" = "#3E6F9F", "#117733" = "#117733", "#dc4c5d" = "#dc4c5d"), labels = c("#3E6F9F" = "Baseline", "#117733" = "Increase", "#dc4c5d" = "Decrease")) + 
                geom_hline(yintercept = 0, color = "black") + 
                theme(axis.text = element_text(color = "black"), axis.ticks = element_line(color = "black"))
                # rescale image and save it
                dpi_web <- 300
                width_pixels <- 1500
                height_pixels <- 1500
                width_inches_web <- width_pixels / dpi_web
                height_inches_web <- height_pixels / dpi_web
                ggsave(filename = "{image_name}", plot = final_plot, width = width_inches_web, height = height_inches_web, dpi = dpi_web)
                ''')
    # execute R script 
    with open(os.devnull, 'w') as nullfile:
        with contextlib.redirect_stdout(nullfile), contextlib.redirect_stderr(nullfile):
            robjects.r(r_script)
    # extract predicted moral sensitivity
    sensitivity = robjects.r['new_pred'][0]
    return sensitivity

def R_to_Py_plot_rescue(resistance, temperature, distance, image_name):
    """ function to execute R script that runs SHAP to create feature importance plot for the situation send in firefighters to rescue """
    r_script = (f'''
                # preprocess data
                data <- read_excel("data/moral_sensitivity_survey_data.xlsx")
                data$situation <- as.factor(data$situation)
                data$temperature <- as.factor(data$temperature)
                data$distance <- as.factor(data$distance)
                data_subset <- subset(data, data$situation == "1" | data$situation == "8")
                data_subset$people <- as.numeric(data_subset$people)
                data_subset <- subset(data_subset, (!data_subset$temperature == "close"))
                data_subset <- data_subset %>% drop_na(distance)
                # fit regression model using subset of data that ensures all assumptions are met
                fit <- lm(sensitivity ~ resistance + temperature + distance, data = data_subset[-c(240, 237, 235, 202, 193, 121, 114, 108, 34, 28, 22),])
                # create prediction dataset
                pred_data <- subset(data_subset[-c(240, 237, 235, 202, 193, 121, 114, 108, 34, 28, 22),], select = c("resistance", "temperature", "distance", "sensitivity"))
                pred_data$temperature <- factor(pred_data$temperature, levels = c("higher", "lower"))
                # fit SHAP explainer
                explainer <- shapr(pred_data, fit)
                # determine baseline moral sensitivity
                baseline_sensitivity <- mean(pred_data$sensitivity)
                # create new dataframe for predictions on unseen data
                new_data <- data.frame(resistance = c({resistance}), temperature = c("{temperature}"), distance = c("{distance}"))
                new_data$temperature <- factor(new_data$temperature, levels = c("higher", "lower"))
                new_data$distance <- factor(new_data$distance, levels = c("large", "small"))
                # generate explanation
                explanation <- shapr::explain(new_data, approach = "ctree", explainer = explainer, prediction_zero = baseline_sensitivity)
                explanation_plot <- plot(explanation, digits = 1, plot_phi0 = TRUE) 
                levels(explanation_plot[["data"]]$sign) <- c("positive", "negative")
                # extract data underlying plot
                data_plot <- explanation_plot[["data"]]
                data_plot$phi <- round(data_plot$phi, 1)
                # extract predicted sensitivity and round it
                new_pred <- round(sum(data_plot$phi), 1)
                # rename some variables for prettier plotting and replace text with symbols
                min <- 'min.'
                temp <- NA
                if ("{temperature}" == 'close') {{ temp <- '<≈ thresh.' }}
                if ("{temperature}" == 'lower') {{ temp <- '&lt; thresh.' }}
                if ("{temperature}" == 'higher') {{ temp <- '&gt; thresh.' }}
                labels <- c(none = "<br> baseline <br> moral <br> sensitivity", 
                resistance = paste("<img src='images/fire_resistance_black.png' width='38' /><br>\n", new_data$resistance, min), 
                temperature = paste("<img src='images/celsius_transparent.png' width='43' /><br>\n", temp), 
                distance = paste("<img src='images/distance_fire_victim_black.png' width='54' /><br>\n", new_data$distance))
                # reorder variables so plot starts with baseline sensitivity and then descending feature importance
                index <- 1
                original_rank <- data_plot$rank[index]
                data_plot$rank[data_plot$rank < original_rank] <- data_plot$rank[data_plot$rank < original_rank] + 1
                data_plot$rank[index] <- 1
                order_indices <- order(data_plot$rank)
                data_plot <- data_plot[order_indices, ]
                data_plot$variable <- factor(data_plot$variable, levels = unique(data_plot$variable))
                # create final plot
                final_plot <- ggplot(data_plot, aes(x = variable, y = phi, fill = ifelse(data_plot$variable == "none", "#3E6F9F", ifelse(data_plot$phi >= 0, "#dc4c5d", "#117733")))) +
                geom_bar(stat = "identity") +
                geom_text(aes(label = ifelse(data_plot$variable=="none", phi, ifelse(data_plot$phi>=0, paste("+", phi, sep=""), paste("-", abs(phi)))),
                y = ifelse(phi >= 0, phi + 0.1, phi - 0.1)), family = "sans-serif", color = "black", size = 4, vjust = ifelse(data_plot$phi >= 0, 0.4, 0.6)) +
                scale_x_discrete(name = NULL, labels = labels) +
                theme(axis.text.x = ggtext::element_markdown()) +
                theme(text = element_text(size = 5, family = "sans-serif"), plot.title = element_text(hjust = 0.5, size = 12, color = "black", face = "bold", margin = margin(b = 5)),
                plot.caption = element_text(size = 12, margin = margin(t = 25), color = "black"), panel.background = element_blank(), axis.text = element_text(size = 12, color = "black"),
                axis.text.y = element_text(color = "black", margin = margin(t = 5)), axis.line = element_line(color = "black"), axis.title = element_text(size = 12), axis.title.y = element_text(color = "black", margin = margin(r = 10), hjust = 0.5),
                axis.title.x = element_text(color = "black", margin = margin(t = 5), hjust = 0.5), panel.grid.major = element_line(color = "#DAE1E7"), panel.grid.major.x = element_blank()) +
                theme(legend.background = element_rect(fill = "white", color = "white"), legend.key = element_rect(fill = "white", color = "white"), legend.text = element_text(size = 12),
                legend.position = "none", legend.title = element_text(size = 12, face = "plain")) +
                labs(y = "Contribution to predicted sensitivity", fill = "") + 
                scale_fill_manual(values = c("#3E6F9F" = "#3E6F9F", "#117733" = "#117733", "#dc4c5d" = "#dc4c5d"), labels = c("#3E6F9F" = "Baseline", "#117733" = "Increase", "#dc4c5d" = "Decrease")) + 
                geom_hline(yintercept = 0, color = "black") + 
                theme(axis.text = element_text(color = "black"), axis.ticks = element_line(color = "black"))
                # rescale image and save it
                dpi_web <- 300
                width_pixels <- 1500
                height_pixels <- 1500
                width_inches_web <- width_pixels / dpi_web
                height_inches_web <- height_pixels / dpi_web
                ggsave(filename = "{image_name}", plot = final_plot, width = width_inches_web, height = height_inches_web, dpi = dpi_web)
                ''')
    # execute R script
    with open(os.devnull, 'w') as nullfile:
        with contextlib.redirect_stdout(nullfile), contextlib.redirect_stderr(nullfile):
            robjects.r(r_script)
    # extract predicted moral sensitivity
    sensitivity = robjects.r['new_pred'][0]
    return sensitivity
    
def load_R_to_Py():
    """ function to load required R libraries """
    r_script = ('''
                # Load libraries
                library('readxl')
                library('ggplot2')
                library('dplyr')
                library("gvlma")
                library('shapr')
                library('ggtext')
                library('tidyr')
                ''')
    robjects.r(r_script)
    
def add_object(locs, image, size, opacity, name, is_traversable, is_movable):
    """ function to add objects to a MATRX world at run time """
    action_kwargs = {}
    add_objects = []
    for loc in locs:
        obj_kwargs = {}
        obj_kwargs['location'] = loc
        obj_kwargs['img_name'] = image
        obj_kwargs['visualize_size'] = size
        obj_kwargs['visualize_opacity'] = opacity
        obj_kwargs['name'] = name
        obj_kwargs['is_traversable'] = is_traversable
        obj_kwargs['is_movable'] = is_movable
        add_objects += [obj_kwargs]
    action_kwargs['add_objects'] = add_objects
    return action_kwargs

def calculate_distances(coordinates1, coordinates2):
    """ function to calculate the Euclidean distance between two coordinates """
    # Unpack the coordinates
    x1, y1 = coordinates1
    x2, y2 = coordinates2
    # calculate Euclidean distance
    euclidean_distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)   
    return euclidean_distance