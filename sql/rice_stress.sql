CREATE TABLE IF NOT EXISTS `rice_stress` (
    `stress_id` NUMERIC(3, 1),
    `stress_name` VARCHAR(21) CHARACTER SET utf8,
    `stress_type` VARCHAR(7) CHARACTER SET utf8,
    `stress_level` VARCHAR(3) CHARACTER SET utf8,
    `description` VARCHAR(125) CHARACTER SET utf8,
    `description_src` VARCHAR(102) CHARACTER SET utf8,
    `recommendation` VARCHAR(1191) CHARACTER SET utf8,
    `recommendation_src` VARCHAR(117) CHARACTER SET utf8
);
INSERT INTO `rice_stress` VALUES (1.0,'blast','biotic',NULL,'Blast is a fungal disease that causes lesions on leaves, stems, and panicles. It can reduce grain yield by up to 70%.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/blast-leaf-collar','1. Plant Resistant Varieties: Use resistant rice varieties; consult local agricultural authorities for updated lists.
2. Crop Management Measures:
*Adjust Planting Time: Sow seeds early in the rainy season.
*Nitrogen Fertilizer Application: Split into multiple treatments to avoid excessive use.
*Field Flooding: Flood the field as frequently as possible.
*Silicon Fertilizers: Apply to silicon-deficient soils. Consider cost-effective sources like rice genotypes high in silicon. Avoid using infected straw as a silicon source.
*Systemic Fungicides: Use judiciously, such as triazoles and strobilurins, particularly during heading stage for effective control.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/blast-leaf-collar'),
	(2.0,'bacterial leaf blight','biotic',NULL,'Bacterial leaf blight is a bacterial disease that causes brown streaks on leaves. It can reduce grain yield by up to 20%.','https://ricetoday.irri.org/a-tool-that-tracks-and-stops-bacterial-blight-outbreaks-in-rice/','* Use balanced amounts of plant nutrients, especially nitrogen.
* Ensure good drainage of fields (in conventionally flooded crops) and nurseries.
* Keep fields clean. Remove weed hosts and plow under rice stubble, straw, rice ratoons and volunteer seedlings, which can serve as hosts of bacteria.
* Allow fallow fields to dry in order to suppress disease agents in the soil and plant residues.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/bacterial-blight?category_id=326'),
	(3.0,'tungro','biotic',NULL,'Tungro is a viral disease that causes yellowing and stunting of plants. It can reduce grain yield by up to 100%.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/tungro','1. No Cure for Infected Plants: Once infected, rice plants cannot be cured from tungro.

2. Preventive Measures are Key: Preventive measures are more effective than direct disease control.

3. Effective Measures Include:
*Use of Resistant Varieties: Plant tungro or leafhopper resistant varieties as the most economical way to manage the disease. Consult local agricultural authorities for updated lists of available varieties.
*Synchronous Planting: Coordinate planting with surrounding farms. Late or delayed planting makes fields more susceptible to tungro and can pose risks in subsequent seasons.
*Adjust Planting Times: Plant when green leafhoppers are not in season or abundant, if such times are known.
*Immediate Stubble Plowing: Plow infected stubbles immediately after harvest to reduce inoculum sources and eliminate breeding sites of green leafhoppers.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/tungro'),
	(4.0,'sheath blight','biotic',NULL,'Sheath blight is a fungal disease that causes brown lesions on leaf sheaths. It can reduce grain yield by up to 15%.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/sheath-blight','* use a reasonable level of fertilizer adapted to the cropping season.
* use reasoned density of crop establishment (direct seeding or transplanting).
* carefully control of weeds, especially on the levees.
* drain rice fields relatively early in the cropping season to reduce sheath blight epidemics.
* use fungicide to treat seeds.
* improve canopy architecture by reducing seeding rate or providing wider plant spacing.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/sheath-blight'),
	(5.0,'brown plant hopper','biotic',NULL,'Brown plant hopper is an insect that sucks sap from plants and transmits tungro virus. It can cause significant yield losses.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/planthopper','1. Preventing Outbreaks:

* Weed Control: Remove weeds from the field and surrounding areas to minimize habitat for brown plant hoppers (BPH).
* Avoid Indiscriminate Insecticide Use: Prevent destroying natural enemies of BPH by avoiding excessive insecticide application.
* Use Resistant Varieties: Opt for resistant rice varieties; consult local agricultural authorities for updated lists.

2.Monitoring and Control Measures:

* Critical Threshold: Act if BPH density exceeds 1 BPH per stem; monitor regularly for increases in numbers.
* Monitoring Methods: Check seedbeds or fields regularly for BPH, using direct observation or light traps at night.
* Mechanical & Physical Measures: Flood seedbeds briefly or sweep them with a net to control BPH.
* Biological Control: Encourage natural enemies of BPH, such as water striders, mirid bugs, spiders, and egg parasitoids, to limit BPH population growth.
* Chemical Control: Apply insecticides in the seedbed only if specific conditions are met, such as high BPH density, outnumbering natural enemies, and when flooding isn''t feasible.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/planthopper'),
	(6.0,'green leaf hopper','biotic',NULL,'Green leaf hopper is an insect that sucks sap from plants and transmits tungro virus. It can cause significant yield losses.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/green-leafhopper','* Use GLH-resistant and tungro-resistant varieties. Contact your local agriculture office for an up-to-date list of available varieties.
* Reduce the number of rice crops to two per year and synchronized crop establishment across farms reduces leafhoppers and other insect vectors.
* Transplant older seedlings (>3 weeks) to reduce viral disease susceptibility transmitted by leafhoppers.
* Plant early within a given planting period, particularly in the dry season to reduce the risk of insect-vector disease.
* Avoid planting during the peak of GLH activity (shown by historical records) to avoid infestation. Light traps can be used to show GLH numbers.
* Apply nitrogen as needed (e.g., using the Leaf Color Chart) to avoid contributing to population outbreaks by applying too much nitrogen, or hindering plant recovery from planthopper damage by applying insufficient nitrogen.
* Control weeds in the field and on the bunds to remove the preferred grassy hosts of GLH and promotes crop vigor.
* Perform crop rotation with a non-rice crop during the dry season to decrease alternate hosts for diseases.
* Intercrop upland rice with soybean to reduce the incidence of leafhoppers on rice.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/green-leafhopper'),
	(7.0,'yellow stem borer','biotic',NULL,'Yellow stem borer is an insect that bores into stems and destroys them. It can cause significant yield losses.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/stem-borer','* Use resistant varieties
* At seedbed and transplanting, handpick and destroy egg masses
* Raise level of irrigation water periodically to submerge the eggs deposited on the lower parts of the plant
* Before transplanting, cut the leaf-top to reduce carry-over of eggs from the seedbed to the field
* Ensure proper timing of planting and synchronous planting, harvest crops at ground level to remove the larvae in stubble, remove stubble and volunteer rice, plow and flood the field
* Encourage biological control agents: braconid, eulophid, mymarid, scelionid, chalcid, pteromalid and trichogrammatid wasps, ants, lady beetles, staphylinid beetles, gryllid, green meadow grasshopper, and mirid, phorid and platystomatid flies, bethylid, braconid, elasmid, eulophid, eurytomid and ichneumonid wasps, carabid and lady bird beetles, chloropid fly, gerrid and pentatomid bugs, ants, and mites,  earwigs, bird, asilid fly, vespid wasp, dragonflies, damselflies, and spiders
* Bacteria and fungi also infect the larvae: mermithid nematode, chalcid, elasmid and eulophid
* Apply nitrogen fertilizer in split following the recommended rate and time of application.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/stem-borer'),
	(8.0,'stem borer','biotic',NULL,'Stem borer is an insect that bores into stems and destroys them. It can cause significant yield losses.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/stem-borer','* Use resistant varieties
* At seedbed and transplanting, handpick and destroy egg masses
* Raise level of irrigation water periodically to submerge the eggs deposited on the lower parts of the plant
* Before transplanting, cut the leaf-top to reduce carry-over of eggs from the seedbed to the field
* Ensure proper timing of planting and synchronous planting, harvest crops at ground level to remove the larvae in stubble, remove stubble and volunteer rice, plow and flood the field
* Encourage biological control agents: braconid, eulophid, mymarid, scelionid, chalcid, pteromalid and trichogrammatid wasps, ants, lady beetles, staphylinid beetles, gryllid, green meadow grasshopper, and mirid, phorid and platystomatid flies, bethylid, braconid, elasmid, eulophid, eurytomid and ichneumonid wasps, carabid and lady bird beetles, chloropid fly, gerrid and pentatomid bugs, ants, and mites,  earwigs, bird, asilid fly, vespid wasp, dragonflies, damselflies, and spiders
* Bacteria and fungi also infect the larvae: mermithid nematode, chalcid, elasmid and eulophid
* Apply nitrogen fertilizer in split following the recommended rate and time of application.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/stem-borer'),
	(9.0,'false smut','biotic',NULL,'False smut is a fungal disease that causes black heads to form on panicles. It can reduce grain yield by up to 10%.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/false-smut','* Keep the field clean.
* Remove infected seeds, panicles, and plant debris after harvest.
* Reduce humidity levels through alternate wetting and drying (AWD) rather than permanently flooding the fields.
* Where possible, perform conservation tillage and continuous rice cropping.
* Use moderate rates of Nitrogen.
* Use certified seeds.
* Resistant varieties have been reported. Contact your local agriculture office for an up-to-date list of available varieties.
* Treat seeds at 52°C for 10 min.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/false-smut'),
	(10.0,'healthy','abiotic','N/A','Healthy rice plants are green and vigorous. They have no signs of disease or pests.','https://www.irri.org/crop-manager','N/A','N/A');
