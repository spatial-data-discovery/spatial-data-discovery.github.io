---
title: Amazon's Last-Mile Delivery Network
---

<!-- VIDEO ON LOOP: see styles.css for formatting -->
<div class="video-wrapper">
  <video id="chenvideo" controls preload="true" autoplay loop muted>
    <source src="https://drive.google.com/uc?id=12LaGn1uNdkuH1JgmxDu0kmbJw0GAEMdd" type="video/mp4" >
  </video>
</div>

## Overview
Amazon is ambitious in taking further control of its supply chain. Since the company launched its first facility for last-mile delivery in 2013, the distribution network has been booming behind services including Prime Now, Whole Foods grocery delivery, and the one-day Prime delivery in plan.

As an e-commerce giant that is estimated to share 38% of the market in 2019[^stats], Amazon's expansion on its distribution network may have a wide influence on delivery firms and other local or online retailers. With its logistics infrastructure, Amazon is threatening the business of delivery firms in the densely populated areas, leaving them with less profitable rural areas. The company may also outcompete other e-commerce providers in terms of speed and efficiency. Thus, visualizing Amazon's delivery network may help business owners and economics researchers understand Amazon's long-term strategy to grow its logistics services capacity and its influence on the e-commerce market.

The animation visualizes the population coverage of Amazon's delivery network in the contiguous U.S. from 2013 to 2020 (projected). The areas reachable by truck from a delivery station within one hour are colored with orange, and the areas that take more than one hour for trucks to travel from a delivery station are colored with dark blue. The variations in population density are revealed through tints.

## Data Description
The population density map uses the 2010 U.S. Census Grids downloaded from Center for International Earth Science Information Network([CIESIN](https://sedac.ciesin.columbia.edu/data/set/usgrid-summary-file1-2010)). For square km grids, with the numbers of people ranging from 0 to 20, a gradual change in tint is on display. Grids with a population greater than or equal to 20 appeal identical in tint.

The addresses of the delivery stations are obtained from MWPVL International([MWPVL](http://www.mwpvl.com/html/amazon_com.html)). A script was used to extract the addresses from a PNG file and another script is used to clean and split the data by year. Both scripts are written in Python[^python]. The addresses are geocoded into location points with ArcMap[^arcmap]. Based on these location points, ArcGIS Online[^arcOn] is used to estimate the 1-hour trucking-time areas and the estimations are exported as shapefiles back into ArcMap for clipping. The clipped raster files are later imported into QGIS[^qgis] for scaling and coloring. The output image sequences are made into an animation using Photoshop[^ps].

<div class="credit-line">
Author: Jiaying Chen.
Last edited: 2019-12-18.
</div>

[^stats]:Bloomberg.com. (2019). Amazon U.S. Online Market Share Estimate Cut to 38% From 47%. Accessed 2019-12-14. Online: https://www.bloomberg.com/news/articles/2019-06-13/emarketer-cuts-estimate-of-amazon-s-u-s-online-market-share.
[^arcmap]: ArcMap Desktop 10.5. Software released through Environmental Systems Research Institute(ESRI). Accessed 2019-11-26. Online: http://desktop.arcgis.com/en/arcmap/
[^python]: Python. Copyright (C) 2001--2019. Python Software Foundation. Accessed 2019-10-28. Online: https://www.python.org/
[^arcOn]: ArcGIS Online. Software released through Environmental Systems Research Institute(ESRI). Accessed 2019-11-26. Online: http://desktop.arcgis.com/en/arcmap/
[^qgis]: QGIS. Software released through CC-BY-SA by the QGIS Development Team. Accessed 2019-11-26. Online: https://www.qgis.org
[^ps]: Photoshop CC 2017. Software released through Adobe. Accessed 2019-11-26. Online: https://www.adobe.com/products/photoshop.html
