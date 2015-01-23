import java.io.*;
//import java.io.Writer.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.*;
//import org.eclipse.swt.widgets.*;

public class NGramExtractorWin extends JFrame implements ActionListener { 
    
    private final String CONFIG = "config";
    private JTextField sourceDirField;
    private JButton dirBtn;
    private JButton extractBtn;
    
    public static void main(String[] args) {
        
        JFrame frame = new NGramExtractorWin();
        frame.setLayout(new FlowLayout());
        frame.setTitle("Extractor");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null);
        frame.pack();
        frame.setVisible(true);
        
    }
    
    public NGramExtractorWin() {
       
        String sourceDir = getSourceDir();
        System.out.println(sourceDir + "fs");
        sourceDirField = new JTextField(sourceDir, 25);        
        add(new JLabel("Source Directory:"));
        add(sourceDirField);
        dirBtn = new JButton("...");
        dirBtn.addActionListener(this);
        dirBtn.setActionCommand("showFileDialogue");
        add(dirBtn);
        extractBtn = new JButton("Extract");
        extractBtn.setActionCommand("extract");
        extractBtn.addActionListener(this);
        add(extractBtn);
        
    }
    
    private String getSourceDir() {
        String path = ""; 
        try {    
            Scanner s = new Scanner(new File(getClass().getResource(CONFIG).toURI()));
            path = s.nextLine();
            s.close();
        }
        catch(Exception e) {
            JOptionPane.showMessageDialog(null, "Configuration file not found.", "Error", JOptionPane.ERROR_MESSAGE);
        }
        return path;        
    }
    
    public void actionPerformed(ActionEvent e) {
        
        String command = e.getActionCommand();
    
        if(command.equals("filedialog")) {
  //          DirectoryDialog fd = new DirectoryDialog();
    //        fd.open();               
        }
        else if(command.equals("extract")) {
        
            NGramExtractor ex = new NGramExtractor(this.sourceDirField.getText());        
            Hashtable<NGram, Integer>[] dict = ex.generateDictionary();
                
            FileDialog fd = new FileDialog(this, "Save the dictionary", FileDialog.SAVE);
            fd.setDirectory("\\");
            fd.setFile("dictionary.txt");
            fd.setVisible(true);
            BufferedWriter writer = null;
            try {
                writer = new BufferedWriter(new FileWriter(fd.getDirectory() + fd.getFile()));
                for(int i = 0; i < dict.length; i++) { // For each of the Hashtables
                    for(NGram key : dict[i].keySet()) {// For each NGram
                        writer.write(key.toString() + "\t" + dict[i].get(key));
                        writer.newLine();
                    }    
                }    
                writer.close();
            }
            catch(IOException ee) {
                //
                System.out.println("IO Exception");
            }
             
            System.out.println("Saved: " + fd.getDirectory() + fd.getFile());
        }
        
           
    }
}
