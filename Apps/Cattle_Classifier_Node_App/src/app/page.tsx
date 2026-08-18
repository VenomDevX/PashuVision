import { Hero } from "@/components/Hero";
import { DatasetSection } from "@/components/DatasetSection";
import { ModelSection } from "@/components/ModelSection";
import { ArchitectureSection } from "@/components/ArchitectureSection";

export default function Home() {
  return (
    <>
      <Hero />
      <DatasetSection />
      <ModelSection />
      <ArchitectureSection />
    </>
  );
}