import gov.nih.nlm.nls.metamap.Ev;
import gov.nih.nlm.nls.metamap.Mapping;
import gov.nih.nlm.nls.metamap.MetaMapApi;
import gov.nih.nlm.nls.metamap.MetaMapApiImpl;
import gov.nih.nlm.nls.metamap.Negation;
import gov.nih.nlm.nls.metamap.PCM;
import gov.nih.nlm.nls.metamap.Result;
import gov.nih.nlm.nls.metamap.Utterance;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class ExtractConceptByMetaMap {

	public static void main(String[] args) throws Exception{
		File dir = new File(".");
		File fin = new File(dir.getCanonicalPath() + File.separator + "t2.txt");
		BufferedReader br = new BufferedReader(new FileReader(fin));	 
		String line = null;
		List<String> list = new ArrayList<String>();
		while ((line = br.readLine()) != null) {
			if (line.length() != 0) {
				list.add(line.replaceAll("[^\\x00-\\x7F]", ""));
			}
		}
		metamapExample(list);
		br.close();
	}
	
	public static void metamapExample(List<String> input) throws Exception {
		PrintWriter writer = new PrintWriter("conceptFromHeadings.csv", "UTF-8");
		writer.println("\"Heading\",\"CUI\",\"Semantic Type\", \"Preferred Name\"");
		//input = "% Change of Co-administered Drug Pharmacokinetic Parameters (90% CI)";
		MetaMapApi api = new MetaMapApiImpl();
		System.out.println("api instanciated");
		for (String str : input) {
			List<Result> resultList = api.processCitationsFromString(str);
			Result result = resultList.get(0);
			List<Negation> negations = result.getNegationList();
			StringBuilder sb = new StringBuilder();
			StringBuilder sbtemp = new StringBuilder();
			StringBuilder sbword = new StringBuilder();
			for (Negation negation : negations){
				System.out.println("conceptposition:" +negation.getConceptPositionList());
				System.out.println("concept pairs:" +negation.getConceptPairList());
				System.out.println("trigger positions: "+negation.getTriggerPositionList());
				System.out.println("trigger: "+negation.getTrigger());
				System.out.println("type: "+negation.getType());
			}
		for (Utterance utterance: result.getUtteranceList()) {
			//System.out.println("Utterance:");
			//System.out.println(" Id: " + utterance.getId());
			sb.append("\"" + utterance.getString() + "\",\"");
			Set<String> hset = new HashSet<String>();
			//System.out.println(" Utterance text: " + utterance.getString());
			//System.out.println(" Position: " + utterance.getPosition());
			for (PCM pcm: utterance.getPCMList()) {
				//System.out.println("Mappings:");
				for (Mapping map: pcm.getMappingList()) {
					//System.out.println("Phrase:");
					//System.out.println(" Map Score: " + map.getScore());
						for (Ev mapEv: map.getEvList()) {
							String currID = mapEv.getConceptId();
							if (!hset.contains(currID)) {
								sb.append(currID +"|");
								hset.add(currID);
								sbtemp.append(mapEv.getSemanticTypes() + "|");
								sbword.append(mapEv.getPreferredName() + "|");
							}
							//System.out.println("Score: " + mapEv.getScore());
							//System.out.println(" Concept Id: " + mapEv.getConceptId());
							//System.out.println(" Concept Name: " + mapEv.getConceptName());
							//System.out.println(" Preferred Name: " + mapEv.getPreferredName());
							//System.out.println(" Matched Words: " + mapEv.getMatchedWords());
							//System.out.println(" Semantic Types: " + mapEv.getSemanticTypes());
							//System.out.println(" MatchMap: " + mapEv.getMatchMap());
							//System.out.println(" MatchMap alt. repr.: " + mapEv.getMatchMapList());
							//System.out.println(" is Head?: " + mapEv.isHead());
							//System.out.println(" is Overmatch?: " + mapEv.isOvermatch());
							//System.out.println(" Sources: " + mapEv.getSources());
							//System.out.println(" Positional Info: " + mapEv.getPositionalInfo());
						}
				}
			}
			/*if (sb.length() > 1) {
				sb.deleteCharAt(sb.length()-1);
				sbtemp.deleteCharAt(sbtemp.length()-1);
				sbword.deleteCharAt(sbword.length()-1);
			}*/
			int index1 = sbtemp.lastIndexOf("|");
			int index2 = sbword.lastIndexOf("|");
			int index3 = sb.lastIndexOf("|");
			if (index1 != -1) {
				sbtemp.deleteCharAt(index1);
			}
			if (index2 != -1) {
				sbword.deleteCharAt(index2);
			}
			if (index3 != -1) {
				sb.deleteCharAt(index3);
			}
			
			sb.append("\",\"" + sbtemp.toString() + "\",\"" + sbword.toString() + "\"");
			writer.println(sb.toString());
		}
		}
		writer.close();
	}
}
