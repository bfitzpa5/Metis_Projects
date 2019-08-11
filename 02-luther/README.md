# Box Office Mojo Regression Analysis

For our second project at Metis, I designed a multivariable regression using data scraped from Box Office Mojo to predict movie ROI.

ROI = Domestic Total Gross / Budget - 1


In this directory you''l find five files:

<table style="width:100%">
  <tr>
    <th>File</th>
    <th>Description</th> 
  </tr>
  <tr>
    <td><i>luther_box_office_mojo_scraper.py</i></td>
    <td>Web Scraper built using Beautiful Soup</td> 
  </tr>
  <tr>
    <td><i>luther_preproc.py</i></td>
    <td>Intital preprocessing of scraped Box Office Mojo data using pandas.</td> 
  </tr>
  <tr>
    <td><i>luther_eda.py</i></td>
    <td>EDA of the Box Office Mojo Data with fun insights into the movie biz!</td> 
  </tr>
  <tr>
    <td><i>luther_model.py</i></td>
    <td>Regression Modeling of Luther Data (Sneak preview, the final model we ended on was a Lasso Regularization with a lot of features!)</td> 
  </tr>
  <tr>
    <td><i>luther_util.py</i></td>
    <td>Helper functions for modeling and EDA</td> 
  </tr>
</table>
